from .api import CS2APIClient
from typing import Dict, Any, Optional
import asyncio
import datetime

class CS2:
    """Main CS2 API wrapper interface"""
    
    def __init__(self):
        self._api = CS2APIClient()
        self.correct_date = None
    
    async def __aenter__(self):
        """Enter async context manager"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager"""
        if self.session:
            await self.session.close()
            self.session = None

    async def close(self):
        """Close context manager"""
        await self._api.close()

    async def get_live_matches(self) -> Dict[str, Any]:
        """
        Get current CS2 matches from BO3.gg API
        
        Returns:
            Dictionary containing live/current matches data with:
            - teams data
            - tournament info
            - AI predictions
            - games details
            - streams info
        
        API Endpoint:
        https://api.bo3.gg/api/v1/matches?scope=widget-matches&page[offset]=0&page[limit]=100&sort=tier_rank,-start_date&filter[matches.status][in]=current&filter[matches.discipline_id][eq]=1&with=teams,tournament,ai_predictions,games,streams
        """
        endpoint = "/matches"
        params = {
            "scope": "widget-matches",
            "page[offset]": 0,  
            "page[limit]": 100,  
            "sort": "tier_rank,-start_date",  
            "filter[matches.status][in]": "current",
            "filter[matches.discipline_id][eq]": 1,  
            "with": "teams,tournament,ai_predictions,games,streams"  
        }
        return await self._api._make_request(endpoint, params)
    
    async def finished(self) -> Dict[str, Any]:
        """
        Get current CS2 matches from BO3.gg API
        
        Returns:
            Dictionary containing live/current matches data with:
            - teams data
            - tournament info
            - AI predictions
            - games details
            - streams info
        
        API Endpoint:
        https://api.bo3.gg/api/v1/matches?scope=widget-matches&page[offset]=0&page[limit]=100&sort=tier_rank,-start_date&filter[matches.status][in]=current&filter[matches.discipline_id][eq]=1&with=teams,tournament,ai_predictions,games,streams
        """
        endpoint = "/matches"
        params = {
            "scope": "widget-matches",
            "page[offset]": 0,  # Changed from string to integer
            "page[limit]": 100,  # Increased from 1 to 100
            "sort": "tier_rank,-start_date",  
            "filter[matches.status][in]": "finished",
            "filter[matches.discipline_id][eq]": 1,  
            "with": "teams,tournament,ai_predictions,games,streams"  
        }
        
        return await self._api._make_request(endpoint, params)
    
    async def get_live_match_snapshot(self, match_id: int) -> Dict[str, Any]:
        """
        Get the last snapshot of a live CS2 match from BO3.gg API
        
        Args:
            match_id: The ID of the match to get snapshot for
            
        Returns:
            Dictionary containing live match snapshot data
            
        API Endpoint: 
        https://api.bo3.gg/api/v1/live/matches/{match_id}/last_snapshot
        """
        endpoint = f"/live/matches/{match_id}/last_snapshot"
        return await self._api._make_request(endpoint)
    
    async def get_todays_matches(self) -> Dict[str, Any]:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        endpoint = "/matches"
        params = {
            "scope": "widget-matches",
            "page[offset]": "0",
            "page[limit]": "100",
            "sort": "tier_rank,-start_date",
            "filter[matches.status][in]": "upcoming",
            "filter[matches.start_date][lt]": f"{today} 23:59",
            "filter[matches.start_date][gt]": f"{today} 00:00",
            "filter[matches.discipline_id][eq]": "1",
            "with": "teams,tournament,ai_predictions,games,streams"
        }
        return await self._api._make_request(endpoint, params)
    
    async def get_match_details(self, slug: str) -> Dict[str, Any]:
        endpoint = f"/matches/{slug}"
        params = {
            "scope": "show-match",
            "with": "games,streams,teams,tournament_deep,stage,ai_predictions"
        }
        return await self._api._make_request(endpoint, params)
    
    async def search_teams(self, query: str, limit: int = 4) -> Dict[str, Any]:
        endpoint = "/filters/teams"
        params = {
            "page[offset]": "0",
            "page[limit]": str(limit),
            "filter[teams.discipline_id][eq]": "1",
            "search_text": query
        }
        return await self._api._make_request(endpoint, params)
    
    async def get_player_matches(self, player_id: int) -> Dict[str, Any]:
        """
        Get matches for a specific player from BO3.gg API
        
        Args:
            player_id: The ID of the player to get matches for
            
        Returns:
            Dictionary containing player's matches data with:
            - teams data
            - tournament info
            - games details
            - streams info
            - match status (finished/upcoming/current)
        
        API Endpoint:
        https://api.bo3.gg/api/v1/matches?scope=widget-matches&page[offset]=0&page[limit]=100&sort=-start_date&filter[matches.status][in]=finished,defwin,upcoming,current&filter[matches.player_ids][overlap]=<player_id>&filter[matches.discipline_id][eq]=1&with=teams,tournament,ai_predictions,games,streams
        """
        endpoint = "/matches"
        params = {
            "scope": "widget-matches",
            "page[offset]": 0,
            "page[limit]": 100,
            "sort": "-start_date",  # Newest matches first
            "filter[matches.status][in]": "finished,defwin,upcoming,current",
            "filter[matches.player_ids][overlap]": str(player_id),
            "filter[matches.discipline_id][eq]": 1,  # CS2
            "with": "teams,tournament,ai_predictions,games,streams"
        }
        return await self._api._make_request(endpoint, params)
    
    async def get_team_matches(
        self,
        team_id: int,
        limit: int = 50,
        days_offset: int = 180,
        end_date: str = None
    ) -> Dict[str, Any]:
        today = datetime.now().date()
        start_date = today - datetime.timedelta(days=days_offset)
        
        if end_date is None:
            end_date = today.isoformat()
        
        endpoint = "/matches"  
        
        params = {
            "scope": "widget-map-pool",
            "page[offset]": "0",
            "page[limit]": str(limit),
            "sort": "-start_date",
            "filter[matches.status][in]": "finished",
            "filter[matches.team_ids][overlap]": str(team_id),
            "filter[matches.start_date][lt]": end_date,
            "filter[matches.start_date][gt]": start_date.isoformat(),
            "filter[matches.discipline_id][eq]": "1",
            "with": "teams,tournament,ai_predictions,games,match_maps"
        }
        
        return await self._make_request(endpoint, params)
    
    async def get_team_upcoming_matches(
        self,
        team_id: int,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get upcoming and current matches for a specific team (exact match to working BO3 API URL)"""
        endpoint = "/matches"  
        
        params = {
            "scope": "widget-matches",
            "page[offset]": "0",
            "page[limit]": str(limit),
            "sort": "-start_date",
            "filter[matches.status][in]": "upcoming,current",
            "filter[matches.team_ids][overlap]": str(team_id),
            "filter[matches.discipline_id][eq]": "1",
            "with": "teams,tournament,ai_predictions,games,streams"
        }
        
        return await self._api._make_request(endpoint, params)
    
    async def get_team_news(self, team_slug: str, limit: int = 5) -> Dict[str, Any]:
        endpoint = "/base_news"
        params = {
            "page[offset]": "0",
            "page[limit]": str(limit),
            "sort": "-published_at",
            "filter[news.rank][in]": "0,1,2",
            "filter[tags.slug][in]": team_slug,
            "filter[news.locale][eq]": "en",
            "filter[base_news.discipline_id][in]": "1",
            "filter[base_news.section][in]": "1"
        }
        return await self._api._make_request(endpoint, params)
    
    async def get_team_stats(self, team_slug: str, days: int = 180) -> Dict[str, Any]:
        today = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        
        general_endpoint = f"/teams/{team_slug}/general_stats"
        general_params = {
            "filter[start_date_to]": today,
            "filter[start_date_from]": from_date
        }
        
        advanced_endpoint = f"/teams/{team_slug}/advanced_stats"
        advanced_params = {
            "filter[begin_at_to]": today,
            "filter[begin_at_from]": from_date
        }
        
        general_stats, advanced_stats = await asyncio.gather(
            self._api._make_request(general_endpoint, general_params),
            self._api._make_request(advanced_endpoint, advanced_params)
        )
        
        return {
            "general_stats": general_stats,
            "advanced_stats": advanced_stats
        }

    async def search_players(self, query: str, limit: int = 4) -> Dict[str, Any]:
        endpoint = "/filters/players"
        params = {
            "page[offset]": "0",
            "page[limit]": str(limit),
            "filter[discipline_id][eq]": "1",
            "with": "country",
            "search_text": query
        }
        return await self._api._make_request(endpoint, params)
    
    async def get_team_data(
        self,
        team_slug: str,  
        locale: str = "en"  
    ) -> Dict[str, Any]:
        """
        Fetches general team data from BO3.GG API.
        
        Args:
            team_slug: The URL-friendly team name (e.g. "natus-vincere")
            locale: Preferred language (e.g. "en", "ru")
        
        Returns:
            Dictionary containing team data
            
        Example:
            >>> await api.get_team_data("natus-vincere")
            {id: 123, name: "Natus Vincere", ...}
        """
        endpoint = f"/teams/{team_slug}"
        params = {
            "prefer_locale": locale
        }
        
        return await self._api._make_request(endpoint, params)
    
    async def get_player_details(self, slug: str) -> Dict[str, Any]:
        endpoint = f"/players/{slug}"
        params = {"prefer_locale": "en"}
        return await self._api._make_request(endpoint, params)
    
    async def get_player_stats(self, slug: str, days: int = 180) -> Dict[str, Any]:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        
        general_endpoint = f"/players/{slug}/general_stats"
        general_params = {
            "filter[start_date_to]": today,
            "filter[start_date_from]": from_date
        }
        
        map_endpoint = f"/players/{slug}/map_stats"
        map_params = {
            "filter[begin_at_to]": today,
            "filter[begin_at_from]": from_date
        }
        
        accuracy_endpoint = f"/players/{slug}/accuracy_stats"
        accuracy_params = {
            "filter[begin_at_to]": today,
            "filter[begin_at_from]": from_date
        }
        
        general_stats, map_stats, accuracy_stats = await asyncio.gather(
            self._api._make_request(general_endpoint, general_params),
            self._api._make_request(map_endpoint, map_params),
            self._api._make_request(accuracy_endpoint, accuracy_params)
        )
        
        return {
            "general_stats": general_stats,
            "map_stats": map_stats,
            "accuracy_stats": accuracy_stats
        }
    
    async def get_team_transfers(self, team_id: int, limit: int = 10) -> Dict[str, Any]:
        endpoint = "/player_transfers"
        params = {
            "join": "teams_deep",
            "page[offset]": "0",
            "page[limit]": str(limit),
            "sort": "-action_date",
            "filter[team_to.id,team_from.id][or]": f"{team_id},{team_id}",
            "with": "teams,player"
        }
        return await self._api._make_request(endpoint, params)
    
    async def get_player_transfers(self, player_id: int, limit: int = 10) -> Dict[str, Any]:
        endpoint = "/player_transfers"
        params = {
            "join": "teams_deep",
            "page[offset]": "0",
            "page[limit]": str(limit),
            "sort": "-action_date",
            "filter[player_id][eq]": str(player_id),
            "filter[is_coach][eq]": "false",
            "with": "teams,player"
        }
        return await self._api._make_request(endpoint, params)
    
