#!/usr/bin/env python3
"""Chao-Pi-Adventure - Main entry point"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chao.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    try:
        from engine.game_engine import GameEngine
        
        logger.info("="*50)
        logger.info("Chao-Pi-Adventure v2.0")
        logger.info("="*50)
        
        engine = GameEngine()
        engine.run()
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
