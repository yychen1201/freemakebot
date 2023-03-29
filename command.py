import discord,os,json,asyncio
from datetime import timedelta
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command

class command(commands.Cog): #更改classname
    def __init__(self,bot):
        self.bot=bot
        

    
    @slash_command(description="設置指令頻道",guild_ids=[1079954205286092862])
    @commands.has_permissions(administrator=True)
    async def set_command(self,ctx,channel:Option(discord.TextChannel,"要設置的頻道")):
        path=f"database/{ctx.guild.id}/command"
        if not os.path.isdir(path):
            os.makedirs(path)
            await ctx.respond("已創建資料,請重新使用指令")
        else:
            with open(f"{path}/command.json","w") as file:
                data={"channel":channel.id}
                json.dump(data,file)
            await ctx.respond("成功設置")
            
            
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.guild.id != 1079954205286092862:
            return
        path=f"database/{message.guild.id}/command"
        if not os.path.isdir(path):
            return
        with open(f"{path}/command.json","r") as file:
            data=json.load(file)
            cid=data["channel"]
        if message.channel.id == cid:
            await asyncio.sleep(30)
            await message.delete()
        
        
 


def setup(bot):
    bot.add_cog(command(bot))