import requests
from bs4 import BeautifulSoup
import json
import os
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('card_collector.log'),
        logging.StreamHandler()
    ]
)

class CardMappings:
    """集中管理所有卡片相關的映射關係"""
    
    FIELD_MAPPING = {
        'LIFE': ('life', lambda x: int(x)),
        'カードタイプ': ('card_type', lambda x: x.strip()),
        'タグ': ('tags', lambda x: [tag.strip('#') for tag in x.strip().split()]),
        'レアリティ': ('rarity', lambda x: x.strip()),
        '収録商品': ('product', lambda x: x.strip()),
        '色': ('color', lambda x: x.strip()),
        'HP': ('hp', lambda x: x.strip()),
        'Bloomレベル': ('bloom_level', lambda x: x.strip()),
        'バトンタッチ': ('baton_touch', lambda x: x.strip())
    }
    
    COLOR_MAPPING = {
        'type_red.png': 'red',
        'type_blue.png': 'blue',
        'type_yellow.png': 'yellow',
        'type_green.png': 'green',
        'type_purple.png': 'purple',
        'type_white.png': 'white'
    }
    
    DETAIL_MAPPING = {
        '色': 'color',
        'HP': 'hp',
        'LIFE': 'life',
        'Bloomレベル': 'bloom_level',
        'バトンタッチ': 'baton_touch'
    }
    
    ICON_MAPPING = {
        'arts_null.png': 'any',
        'arts_red.png': 'red',
        'arts_blue.png': 'blue',
        'arts_yellow.png': 'yellow',
        'arts_green.png': 'green',
        'arts_purple.png': 'purple',
        'arts_white.png': 'white'
    }
    
    KEYWORD_SUBTYPES = {
        'bloomEF.png': 'ブルームエフェクト',
        'collabEF.png': 'コラボエフェクト',
        'gift.png': 'ギフト'
    }


class CardParser:
    """負責解析卡片數據的類"""
    
    def __init__(self, card_element):
        self.card_element = card_element
        self.card_data = {}
    
    def parse_basic_info(self):
        """解析基本信息（編號、名稱、圖片）"""
        try:
            self.card_data['number'] = self._get_text('p', 'number')
            self.card_data['name'] = self._get_text('p', 'name')
            
            img_element = self.card_element.find('div', class_='img').find('img')
            if img_element:
                self.card_data['image_url'] = 'https://hololive-official-cardgame.com' + img_element['src']
                self.card_data['image_alt'] = img_element.get('alt', '')
        except Exception as e:
            logging.error(f"Error parsing basic info: {e}")
    
    def parse_card_info(self):
        """解析卡片信息（類型、標籤等）"""
        try:
            info_dl = self.card_element.find('div', class_='info').find('dl')
            if not info_dl:
                return
            
            for dt, dd in zip(info_dl.find_all('dt'), info_dl.find_all('dd')):
                field = dt.text.strip()
                if field in CardMappings.FIELD_MAPPING:
                    key, transform = CardMappings.FIELD_MAPPING[field]
                    self.card_data[key] = transform(dd.text)
        except Exception as e:
            logging.error(f"Error parsing card info: {e}")
    
    def parse_detail_info(self):
        """解析詳細信息（顏色、HP等）"""
        try:
            info_detail = self.card_element.find('dl', class_='info_Detail')
            if not info_detail:
                return
            
            for dt, dd in zip(info_detail.find_all('dt'), info_detail.find_all('dd')):
                key = dt.text.strip()
                if key not in CardMappings.DETAIL_MAPPING:
                    continue
                    
                field_name = CardMappings.DETAIL_MAPPING[key]
                value = dd.text.strip()
                
                if value:
                    self.card_data[field_name] = value
        except Exception as e:
            logging.error(f"Error parsing detail info: {e}")
    
    def parse_skills(self):
        """解析所有技能"""
        try:
            skills = []
            
            # 解析支援效果
            if self._is_support_card():
                support_skill = self._parse_support_skill()
                if support_skill:
                    skills.append(support_skill)
            
            # 解析其他技能
            for skill_div in self.card_element.find_all('div', class_=['oshi', 'sp', 'arts', 'keyword']):
                skill = self._parse_skill(skill_div)
                if skill:
                    skills.append(skill)
            
            if skills:
                self.card_data['skills'] = skills
        except Exception as e:
            logging.error(f"Error parsing skills: {e}")
    
    def _get_text(self, tag, class_name):
        """獲取指定元素的文本"""
        element = self.card_element.find(tag, class_=class_name)
        return element.text.strip() if element else ''
    
    def _parse_color(self, element):
        """解析顏色信息"""
        img = element.find('img')
        if img:
            src = img.get('src', '')
            return next((color for img_name, color in CardMappings.COLOR_MAPPING.items() 
                       if img_name in src), None)
        return None
    
    def _parse_baton_touch(self, element):
        """解析接力信息
        返回接力位置列表，每個位置可以是：
        - 'any': 表示可以接任意顏色（顯示為null圖標）
        - 'no': 表示該位置不能接力（沒有圖標）
        """
        result = []
        icons = element.find_all('img')
        
        # 如果沒有任何圖標，表示不能接力
        if not icons:
            return ['no']
            
        # 解析每個圖標
        for img in icons:
            src = img.get('src', '')
            for icon_src, color in CardMappings.ICON_MAPPING.items():
                if icon_src in src:
                    result.append(color)
                    break
                
        return result 
    
    def _is_support_card(self):
        """檢查是否為支援卡片"""
        return 'card_type' in self.card_data and 'サポート' in self.card_data['card_type']
    
    def _parse_support_skill(self):
        """解析支援技能"""
        info_dl = self.card_element.find('div', class_='info').find('dl')
        if not info_dl:
            return None
            
        for dt, dd in zip(info_dl.find_all('dt'), info_dl.find_all('dd')):
            if dt.text.strip() == '能力テキスト':
                return {
                    'type': 'サポート効果',
                    'name': dd.text.strip()
                }
        return None
    
    def _parse_skill(self, skill_div):
        """解析單個技能"""
        try:
            skill_type = skill_div.find('p').text.strip()
            skill_text = skill_div.find_all('p')[-1].text.strip()
            
            skill_data = {'type': skill_type}
            
            # 解析關鍵字技能的子類型
            if skill_type == 'キーワード':
                subtype = self._parse_keyword_subtype(skill_div)
                if subtype:
                    skill_data['subtype'] = subtype
            
            # 解析技能文本
            skill_data.update(self._parse_skill_text(skill_text, skill_type))
            
            # 只在非推し技能時解析技能圖標
            if skill_type not in ['推しスキル', 'SP推しスキル', 'キーワード']:
                icons = self._parse_skill_icons(skill_div)
                if icons:
                    skill_data['icons'] = icons
            
            return skill_data
        except Exception as e:
            logging.error(f"Error parsing skill: {e}")
            return None
    
    def _parse_keyword_subtype(self, skill_div):
        """解析關鍵字技能的子類型"""
        img = skill_div.find('img')
        if img:
            src = img.get('src', '')
            return next((subtype for img_name, subtype in CardMappings.KEYWORD_SUBTYPES.items() 
                       if img_name in src), None)
        return None
    
    def _parse_skill_text(self, skill_text, skill_type):
        """解析技能文本"""
        if skill_type == 'アーツ':
            return self._parse_arts_skill(skill_text)
        elif skill_type == 'キーワード':
            return self._parse_keyword_skill(skill_text)
        else:
            return {'text': skill_text}
    
    def _parse_arts_skill(self, skill_text):
        """解析アーツ技能文本"""
        parts = skill_text.split('\n', 1)
        first_part = parts[0].strip()
        
        import re
        match = re.match(r'^(.+?)\s*(\d+\+?|\?\+?)$', first_part)
        if not match:
            return {'text': skill_text}
        
        result = {
            'name': match.group(1).strip(),
            'dmg': match.group(2).strip()
        }
        
        if len(parts) > 1 and parts[1].strip():
            result['description'] = parts[1].strip()
        
        return result
    
    def _parse_keyword_skill(self, skill_text):
        """解析キーワード技能文本"""
        parts = skill_text.split('\n', 1)
        return {
            'name': parts[0].strip(),
            'description': parts[1].strip() if len(parts) > 1 else ''
        }
    
    def _parse_skill_icons(self, skill_div):
        """解析技能圖標"""
        icons = []
        # 先處理主要圖標
        for img in skill_div.select('img:not(.tokkou img)'):  # 排除tokkou中的圖標
            src = img.get('src', '')
            for icon_src, color in CardMappings.ICON_MAPPING.items():
                if icon_src in src:
                    icons.append(color)
                    break
        
        result = {'main': icons if icons else None}
        
        # 處理tokkou圖標
        tokkou_span = skill_div.find('span', class_='tokkou')
        if tokkou_span and tokkou_span.find('img'):
            tokkou_alt = tokkou_span.find('img').get('alt', '')
            if tokkou_alt:
                result['tokkou'] = [tokkou_alt]
                
        return result
    
    def parse_id(self):
        """解析卡片的唯一識別碼"""
        image_url = self.card_data.get('image_url', '')
        card_id = image_url.split('/')[-1].split('.')[0] if image_url else f"{self.card_data['number']}-{self.card_data.get('rarity', '')}"
        self.card_data['id'] = card_id
        return card_id


class CardCollector:
    def __init__(self):
        self.base_url = 'https://hololive-official-cardgame.com/cardlist/cardsearch_ex'
        self.headers = {
            'Cookie': 'cardlist_view=text; cardlist_search_sort=new'
        }
        self.data_file = 'card_data.json'
        self.existing_cards = self.load_existing_data()

    def load_existing_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Error loading existing data: {e}")
            return {}

    def save_data(self, data):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, ensure_ascii=False, indent=2, fp=f)
            logging.info("Data saved successfully")
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def parse_card(self, card_element):
        """解析卡片元素並返回卡片數據"""
        try:
            parser = CardParser(card_element)
            parser.parse_basic_info()
            parser.parse_card_info()
            parser.parse_detail_info()
            parser.parse_skills()
            card_key = parser.parse_id()
            return parser.card_data, card_key
        except Exception as e:
            logging.error(f"Error parsing card: {e}")
            return None, None

    def fetch_cards(self):
        page = 1
        all_cards = self.existing_cards.copy()
        total_processed_count = 0
        total_new_cards_count = 0
        
        while True:
            try:
                logging.info(f"Processing page {page}")
                params = {
                    'keyword': '',
                    'attribute[0]': 'all',
                    'expansion_name': '',
                    'card_kind[0]': 'all',
                    'rare[0]': 'all',
                    'bloom_level[0]': 'all',
                    'parallel[0]': 'all',
                    'page': str(page)
                }
                
                response = requests.get(self.base_url, headers=self.headers, params=params)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                cards = soup.find_all('li', class_='ex-item')
                
                if not cards:
                    logging.info(f"No more cards found on page {page}")
                    break
                
                page_processed_count = 0
                page_new_cards_count = 0
                
                for card_element in cards:
                    page_processed_count += 1
                    card_data, card_key = self.parse_card(card_element)
                    if card_data:
                        if card_key not in all_cards:
                            all_cards[card_key] = card_data
                            page_new_cards_count += 1
                            logging.info(f"Added new card: {card_key}")
                
                total_processed_count += page_processed_count
                total_new_cards_count += page_new_cards_count
                
                logging.info(f"Page {page} completed. Cards processed: {page_processed_count}, New cards: {page_new_cards_count}")
                
                # 保存每頁的進度
                self.save_data(all_cards)
                
                # 繼續下一頁
                page += 1
                time.sleep(1)  # 避免請求過於頻繁
                
            except Exception as e:
                logging.error(f"Error on page {page}: {e}")
                break
        
        # 最終總結
        logging.info(f"Finished processing all pages. Total cards processed: {total_processed_count}, Total new cards: {total_new_cards_count}")
        print(f"\nFinal Summary:")
        print(f"Total pages processed: {page}")
        print(f"Total cards processed: {total_processed_count}")
        print(f"New cards added: {total_new_cards_count}")
        print(f"Existing cards: {len(self.existing_cards)}")
        print(f"Total cards in database: {len(all_cards)}")

def run_collector():
    collector = CardCollector()
    collector.fetch_cards()

def main():
    logging.info("Card Collector started")
    
    # Run immediately on start
    run_collector()

if __name__ == "__main__":
    main()
