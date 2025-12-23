import sys
import json
import asyncio
from howlongtobeatpy import HowLongToBeat

async def list_commands(game_name):
    hltb = HowLongToBeat()
    results = await hltb.async_search(game_name)
    
    if results is not None and len(results) > 0:
        best_match = results[0]
        output = {
            "name": best_match.game_name,
            "main_story": best_match.main_story,
            "main_extra": best_match.main_extra,
            "completionist": best_match.completionist,
            "all_styles": best_match.all_styles,
            "similarity": best_match.similarity
        }
        print(json.dumps(output))
    else:
        print(json.dumps({"error": "Not found"}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No game name provided"}))
        sys.exit(1)
        
    game_name = sys.argv[1]
    asyncio.run(list_commands(game_name))
