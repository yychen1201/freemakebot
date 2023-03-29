import discord,os,json,asyncio
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command

class comment(commands.Cog): #更改classname
    def __init__(self,bot):
        self.bot=bot
        
        
    @slash_command(description="發送評價",guild_ids=[1079954205286092862])
    async def comment(self,ctx,
            內容:Option(str,"要發送的內容"),
            星星數:Option(int,"請輸入1-5", min_value=1, max_value=5, default=5)):
        if 星星數 == 1:
            star = "⭐"
        if 星星數 == 2:
            star = "⭐⭐"
        if 星星數 == 3:
            star = "⭐⭐⭐"
        if 星星數 == 4:
            star = "⭐⭐⭐⭐"
        if 星星數 == 5:
            star = "⭐⭐⭐⭐⭐"
        user = ctx.author
        channel = self.bot.get_channel(1085058234391474246)
        role = ctx.guild.get_role(1082213858556530738)
        if role in ctx.author.roles:
            embed = discord.Embed(title="評價系統",description=f"星星數:{star}\n{內容}")
            webhook = await channel.create_webhook(name="評價系統")
            await webhook.send(embed=embed,username=ctx.author.name, avatar_url=user.display_avatar.url)
            await ctx.respond("發送成功")
            await webhook.delete()
            await ctx.author.remove_roles(role,reason=f"評價身分移除")
        else:
            await ctx.respond(f"必須擁有{role.mention}才能發送")
        
    @slash_command(description="發送嵌入訊息",guild_ids=[1079954205286092862])
    async def embed(self,ctx,ti,de):
        embed = discord.Embed(title=ti,description=de.replace("{n}","\n"))
        await ctx.send(embed=embed)
        
        
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.guild.id != 1079954205286092862:
            return
        no = "中國","共產","分裂","中共"
        ms = f"{message.content}"
        if "中共" in ms:
            await message.delete()
            member = message.author
            return await member.send("您使用的用詞已被禁止")
        if "共產" in ms:
            await message.delete()
            member = message.author
            return await member.send("您使用的用詞已被禁止")
        if "分裂" in ms:
            await message.delete()
            member = message.author
            return await member.send("您使用的用詞已被禁止")
        if "國" in ms:
            await message.delete()
            member = message.author
            return await member.send("您使用的用詞已被禁止")
        if "習近平" in ms:
            await message.delete()
            member = message.author
            return await member.send("您使用的用詞已被禁止")
        if "黨" in ms:
            await message.delete()
            member = message.author
            return await member.send("您使用的用詞已被禁止")
        if "習維尼" in ms:
            await message.delete()
            member = message.author
            return await member.send("您使用的用詞已被禁止")
 
        
        
            


            


def setup(bot):
    bot.add_cog(comment(bot))
