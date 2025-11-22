#!/usr/bin/env python3
"""
RuTracker Bot - Russian-Language Torrent Seeding
Distributes decoys on Russian torrent trackers with localized descriptions
Part of the LeakHunter Swarm intelligence system
"""

import json
import hashlib
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RuTrackerBot:
    """Automated bot for seeding decoys on RuTracker with Russian descriptions"""
    
    def __init__(self, bot_id: Optional[str] = None):
        self.bot_id = bot_id or "rutracker_bot_001"
        self.account = "strategickhaos_uploader"
        self.uploads = []
        self.forum_posts = []
        
        # Russian language templates
        self.templates = {
            "title": [
                "Strategickhaos - Полный набор AI моделей v{version}",
                "Суверенная архитектура - Комплект разработчика v{version}",
                "AI Агенты Strategickhaos - Полная версия v{version}"
            ],
            "description": [
                "Полный набор AI моделей и инструментов от Strategickhaos DAO.\n"
                "Включает: нейронные сети, векторные базы, Docker контейнеры.\n"
                "Размер: {size} ГБ | Версия: {version}",
                
                "Комплексная система суверенной AI архитектуры.\n"
                "Содержит: LLM модели, фреймворки, готовые агенты.\n"
                "Объем: {size} ГБ | Релиз: {version}"
            ]
        }
    
    def generate_russian_post(self, name: str, size_gb: float, version: str) -> Dict:
        """Generate Russian-language forum post"""
        title_template = random.choice(self.templates["title"])
        desc_template = random.choice(self.templates["description"])
        
        title = title_template.format(version=version)
        description = desc_template.format(size=f"{size_gb:.1f}", version=version)
        
        return {
            "title": title,
            "description": description,
            "language": "ru"
        }
    
    def create_upload(self, name: str, size_gb: float, watermark: str,
                     decoy_version: str = "v2") -> Dict:
        """Create a new RuTracker upload"""
        torrent_id = len(self.uploads) + 1000000  # Simulate RuTracker ID
        infohash = hashlib.sha1(f"{name}:{watermark}".encode()).hexdigest()
        
        # Generate Russian post
        post = self.generate_russian_post(name, size_gb, decoy_version)
        
        upload = {
            "torrent_id": torrent_id,
            "infohash": infohash,
            "name": name,
            "size_gb": size_gb,
            "watermark": watermark,
            "decoy_version": decoy_version,
            "post_title": post["title"],
            "post_description": post["description"],
            "uploaded_by": self.account,
            "uploaded_at": datetime.utcnow().isoformat(),
            "category": "Программы и Дизайн » Программы для Linux",
            "seeders": 0,
            "leechers": 0,
            "completed": 0,
            "status": "active"
        }
        
        self.uploads.append(upload)
        logger.info(f"Created RuTracker upload: {post['title']} (ID: {torrent_id})")
        return upload
    
    def update_torrent_stats(self, torrent_id: int, seeders: int = 0, 
                            leechers: int = 0, completed: int = 0):
        """Update torrent statistics"""
        for upload in self.uploads:
            if upload["torrent_id"] == torrent_id:
                upload["seeders"] = seeders
                upload["leechers"] = leechers
                upload["completed"] += completed
        
        logger.info(f"Stats updated for torrent {torrent_id}: "
                   f"S:{seeders} L:{leechers} C:{completed}")
    
    def post_forum_update(self, torrent_id: int, message: str):
        """Post update message in forum thread"""
        post = {
            "torrent_id": torrent_id,
            "posted_by": self.account,
            "message": message,
            "posted_at": datetime.utcnow().isoformat()
        }
        
        self.forum_posts.append(post)
        logger.info(f"Forum post created for torrent {torrent_id}")
        return post
    
    def get_bot_statistics(self) -> Dict:
        """Get bot statistics"""
        total_seeders = sum(u["seeders"] for u in self.uploads)
        total_completed = sum(u["completed"] for u in self.uploads)
        
        return {
            "bot_id": self.bot_id,
            "account": self.account,
            "total_uploads": len(self.uploads),
            "active_uploads": len([u for u in self.uploads if u["status"] == "active"]),
            "total_seeders": total_seeders,
            "total_completed": total_completed,
            "forum_posts": len(self.forum_posts)
        }
    
    def print_status(self):
        """Print formatted bot status"""
        stats = self.get_bot_statistics()
        
        print("\n" + "="*60)
        print("🇷🇺 RUTRACKER BOT STATUS")
        print("="*60)
        print(f"Bot ID: {stats['bot_id']}")
        print(f"Account: {stats['account']}")
        print(f"Total Uploads: {stats['total_uploads']}")
        print(f"Active Uploads: {stats['active_uploads']}")
        print(f"Total Seeders: {stats['total_seeders']}")
        print(f"Total Completed: {stats['total_completed']}")
        print(f"Forum Posts: {stats['forum_posts']}")
        print("="*60 + "\n")
        
        if self.uploads:
            print("📤 Recent Uploads:")
            for i, upload in enumerate(self.uploads[-5:], 1):
                print(f"  {i}. [{upload['torrent_id']}] {upload['post_title'][:50]}...")
                print(f"      S: {upload['seeders']} L: {upload['leechers']} "
                      f"C: {upload['completed']}")
    
    def generate_magnet_link(self, torrent_id: int) -> str:
        """Generate magnet link for torrent"""
        for upload in self.uploads:
            if upload["torrent_id"] == torrent_id:
                return (f"magnet:?xt=urn:btih:{upload['infohash']}"
                       f"&dn={upload['name']}"
                       f"&tr=http://bt.rutracker.cc/ann")
        return ""
    
    def save_bot_data(self, output_path: str = "swarm_agents/leakhunter/rutracker_bot.json"):
        """Save bot data to file"""
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        data = {
            "bot_statistics": self.get_bot_statistics(),
            "uploads": self.uploads,
            "forum_posts": self.forum_posts[-50:],  # Last 50 posts
            "exported_at": datetime.utcnow().isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Bot data saved to {output_path}")


def main():
    """Main execution for testing"""
    # Initialize RuTracker bot
    bot = RuTrackerBot()
    
    print("🚀 Initializing RuTracker Bot...")
    
    # Create some uploads
    uploads = [
        bot.create_upload("Strategickhaos-AI-Complete-v2.tar.gz", 105.5, "watermark_ru_001", "v2.0"),
        bot.create_upload("Sovereignty-Architecture-Full.7z", 82.3, "watermark_ru_002", "v2.1"),
        bot.create_upload("AI-Agents-Bundle-Russian.zip", 65.7, "watermark_ru_003", "v2.0")
    ]
    
    # Update stats to simulate activity
    bot.update_torrent_stats(uploads[0]["torrent_id"], seeders=12, leechers=45, completed=156)
    bot.update_torrent_stats(uploads[1]["torrent_id"], seeders=8, leechers=23, completed=89)
    bot.update_torrent_stats(uploads[2]["torrent_id"], seeders=5, leechers=15, completed=42)
    
    # Post some forum updates
    bot.post_forum_update(uploads[0]["torrent_id"], 
                         "Обновление: добавлены новые модели. Раздача активна!")
    
    # Generate magnet links
    for upload in uploads:
        magnet = bot.generate_magnet_link(upload["torrent_id"])
        print(f"✅ Magnet: {magnet[:70]}...")
    
    # Display status
    bot.print_status()
    
    # Save data
    bot.save_bot_data()
    print("\n✅ Bot data saved")


if __name__ == "__main__":
    main()
