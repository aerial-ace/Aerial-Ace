from datetime import timedelta

from discord import AutoShardedBot, Message, Member, utils

from managers import mongo_manager
from helpers import battle_helper
import config

class BattleManager:

    expire_time = 10 * 60 # After how many minutes should the keys be cleared.
    _open_battles: dict[int, list[dict]] = {}

    async def clear_user(self, guild_id: int, index: int):
        """Run if a user start another battle and current battle hasnot ended."""
        if self._open_battles.get(guild_id, []):
            return self._open_battles[guild_id].pop(index)

    async def clear_old_logs(self):
        """Clear old battle data if the time has passed too much."""

        pop_entries = []
        for server in self._open_battles:
            for index, entry in enumerate(self._open_battles[server]):
                if entry['expire'] <= utils.utcnow():
                    pop_entries.insert(0, index)

            for index in pop_entries:
                self._open_battles[server].pop(index)

    async def logging_enabled(self, server_id: str) -> bool:
        data_cursor = await mongo_manager.manager.get_all_data("servers", {"server_id": server_id})
        if data_cursor[0].get("auto_battle_logging", 1) != 1:
            return False
        return True
    
    async def get_user_id(self, name: str, members: list[Member]) -> int:
        user = utils.find(lambda m: m.name == name, members)
        if user:
            return user.id
        return False
    
    async def main_handler(self, bot: AutoShardedBot, message: Message):
        bot_member: Member = message.guild.get_member(bot.user.id)

        # return if bot is not allowed to send messages in this channel
        if message.channel.permissions_for(bot_member).send_messages is False:
            return
        
        guild_id = message.guild.id

        logging_enabled = await self.logging_enabled(str(guild_id))

        if not logging_enabled:
            return
        
        embed = message.embeds
        if not embed:
            # Also check for condition like cancel and won.

            # Cancel
            if message.content.strip().startswith(f"<@{config.POKETWO_ID}>"):
                index = await self.get_pair(guild_id, message.author.id)
                                
                if index is False:
                    return
                
                if "x" not in message.content.lower() and "cancel" not in message.content.lower():
                    return 

                battle_cancel_keywords = ["duel ", "battle "]

                for _keyword in battle_cancel_keywords:
                    if _keyword in message.content:
                        await self.clear_user(guild_id, index)
                        await message.channel.send('Logging Cancelled.')
                else:
                    return
                
            # Won
            if message.author.id == int(config.POKETWO_ID):
                if "won the battle!" in message.content.lower():
                    winner = message.mentions[0].id
                else:
                    if "has won." in message.content:
                        winner = int(message.content.removesuffix("> has won.").split()[-1].removeprefix("<@"))
                    else:
                        return
                    
                index = await self.get_pair(guild_id, winner)
                if index is False:
                    return 
                
                pair = self._open_battles.get(guild_id, [])[index]
                
                await self.clear_user(guild_id, index)

                if winner not in pair.values():
                    return

                loser = pair['target'] if winner == pair['challenger'] else pair['challenger']

                winner_name = pair['challenger_n'] if winner == pair['challenger'] else pair['target_n']
                loser_name = pair['target_n'] if winner == pair['challenger'] else pair['challenger_n']

                reply = await battle_helper.register_battle_log(guild_id, str(winner), str(loser), winner_name, loser_name)

                await message.channel.send(reply)
            return
        
        if str(message.author.id) != config.POKETWO_ID:
            return
        
        embed_data = embed[0].to_dict()

        if embed_data.get('title', None) and embed_data['title'] != 'Choose your party':
            return

        if embed_data.get('fields')[0]['value'] != 'None' or embed_data.get('fields')[1]['value'] != 'None':
            return
        

        challenger_name = embed_data['fields'][0]['name'][:-8]
        challenger_id = await self.get_user_id(challenger_name, message.guild.members)

        target_name = embed_data['fields'][1]['name'][:-8]
        target_id = await self.get_user_id(target_name, message.guild.members)

        if not challenger_id or not target_id:
            return        
        
        await message.channel.send(
            "> Auto Battle Log Session Started! \n**NOTE: **Auto Battle Logging Module is coming out of beta and will be released as a premium feature! If you want to continue using it, please support aerial ace on patron.")


        # Check if he already exits and remove it 
        for id in [challenger_id, target_id]:
            check = await self.get_pair(guild_id, id)
            if check is not False:
                await self.clear_user(guild_id, check)

        # Add a user to existing list
        if guild_id in self._open_battles:
            self._open_battles[guild_id].append(
                {
                    'challenger': challenger_id, 
                    'target': target_id,
                    'challenger_n': challenger_name,
                    'target_n': target_name,
                    'expire': utils.utcnow() + timedelta(seconds=self.expire_time)
                }
            )
        else:
            self._open_battles[guild_id] = [
                {
                    'challenger': challenger_id, 
                    'target': target_id, 
                    'challenger_n': challenger_name,
                    'target_n': target_name,
                    'expire': utils.utcnow() + timedelta(seconds=self.expire_time)
                }
            ]
        
    async def get_pair(self, guild_id: int, id: int) -> int:
        """Return the pair index number."""
        guild_data = self._open_battles.get(guild_id, [])
        if not guild_data:
            return False
        
        for index, data in enumerate(guild_data):
            if id in (data['challenger'], data['target']):
                return index
        
        return False