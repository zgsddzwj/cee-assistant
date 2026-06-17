# spiders/async_spider.py
"""异步爬虫基类 - 支持并发请求和连接池

特性：
1. 异步HTTP请求（aiohttp）
2. 连接池和会话复用
3. 并发控制（信号量）
4. 自动重试和错误处理
5. 请求速率限制
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import logging
import time
import random

logger = logging.getLogger(__name__)

class AsyncSpider:
    """异步爬虫基类"""
    
    def __init__(
        self,
        max_concurrent: int = 5,
        timeout: int = 15,
        delay_min: float = 1.0,
        delay_max: float = 3.0,
        max_retries: int = 3,
        headers: Optional[Dict[str, str]] = None
    ):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.max_retries = max_retries
        
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore: Optional[asyncio.Semaphore] = None
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        connector = aiohttp.TCPConnector(
            limit=20,  # 连接池大小
            limit_per_host=5,  # 每个主机的连接数
            ttl_dns_cache=300,  # DNS缓存时间
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self.headers,
        )
        
        self.semaphore = asyncio.Semaphore(self.max_concurrent)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def fetch(self, url: str, retries: int = 0) -> Optional[str]:
        """异步获取页面内容"""
        async with self.semaphore:
            try:
                # 添加随机延迟
                delay = random.uniform(self.delay_min, self.delay_max)
                await asyncio.sleep(delay)
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        logger.warning(f"HTTP {response.status} for {url}")
                        return None
                        
            except asyncio.TimeoutError:
                if retries < self.max_retries:
                    logger.warning(f"Timeout for {url}, retrying ({retries + 1}/{self.max_retries})")
                    await asyncio.sleep(2 ** retries)  # 指数退避
                    return await self.fetch(url, retries + 1)
                else:
                    logger.error(f"Max retries exceeded for {url}")
                    return None
                    
            except Exception as e:
                logger.error(f"Error fetching {url}: {e}")
                return None
    
    async def fetch_multiple(self, urls: List[str]) -> Dict[str, Optional[str]]:
        """并发获取多个页面"""
        tasks = [self.fetch(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            url: result if not isinstance(result, Exception) else None
            for url, result in zip(urls, results)
        }
    
    async def fetch_with_callback(
        self,
        urls: List[str],
        callback: Callable[[str, str], Any],
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[Any]:
        """并发获取并处理结果"""
        results = []
        total = len(urls)
        
        for i, url in enumerate(urls):
            html = await self.fetch(url)
            if html:
                result = callback(url, html)
                results.append(result)
            
            if progress_callback:
                progress_callback(i + 1, total)
        
        return results


class AsyncExamBoardSpider(AsyncSpider):
    """异步考试院爬虫"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provincial_urls = {
            'beijing': 'https://www.bjeea.cn/html/gkgxx/',
            'shanghai': 'https://www.shmeea.edu.cn/',
            'guangdong': 'https://eea.gd.gov.cn/',
            'jiangsu': 'https://www.jseea.cn/',
            'zhejiang': 'https://www.zjzs.net/',
        }
    
    async def crawl_province(self, province: str) -> Dict[str, Any]:
        """爬取单个省份数据"""
        url = self.provincial_urls.get(province)
        if not url:
            return {'province': province, 'error': 'URL not found'}
        
        html = await self.fetch(url)
        if not html:
            return {'province': province, 'error': 'Failed to fetch'}
        
        # 解析数据（简化版）
        return {
            'province': province,
            'html_length': len(html),
            'timestamp': datetime.now().isoformat(),
        }
    
    async def crawl_all(self) -> List[Dict[str, Any]]:
        """并发爬取所有省份"""
        tasks = [
            self.crawl_province(province)
            for province in self.provincial_urls.keys()
        ]
        return await asyncio.gather(*tasks)


# 使用示例
async def main():
    """异步爬虫使用示例"""
    async with AsyncExamBoardSpider() as spider:
        results = await spider.crawl_all()
        for result in results:
            print(f"{result['province']}: {result.get('html_length', 0)} bytes")


if __name__ == '__main__':
    asyncio.run(main())
