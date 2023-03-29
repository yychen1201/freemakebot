import discord
from datetime import timedelta
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command


class ticket_embed_button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout= None)
        
    @discord.ui.button(label="刪除頻道",custom_id="close_button",style=discord.ButtonStyle.green)
    async def confirm_button(self, button, interaction):
        try:
            return await interaction.channel.delete()
        except:
            return await interaction.response.send_message("刪除頻道失敗")
        
    

class ticket(commands.Cog): #更改classname
    def __init__(self,bot):
        self.bot=bot
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ticket_embed_button())
        
    @slash_command(description="約談用戶",guild_ids=[1079954205286092862])
    async def chat(self,ctx,member:Option(discord.Member,"要約談的用戶")):
        if ctx.author.guild_permissions.manage_channels:
            overwrites = {
                ctx.author:discord.PermissionOverwrite(read_messages=True),
                member: discord.PermissionOverwrite(read_messages=True),
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)}
            ticket = await ctx.guild.create_text_channel(name=f"chat-{member.name}", category=ctx.channel.category, overwrites=overwrites)
            embed = discord.Embed(title=f"`{ctx.author}`為`{member}`建立的客服單", description=f"這是一張約談單由{ctx.author}建立", color=discord.Colour.random())
            await ticket.send(embed=embed,view=ticket_embed_button())
            await ticket.send(content=member.mention, delete_after=0)
            await ctx.respond(f"你的CHAT在{ticket.mention}")
        else:
            await ctx.respond("沒有適當權限, 您應至少具備 **管理頻道(Manage Channels)** 權限以使用此指令")
            
            
            
    @slash_command(description="反應bug給開發者")
    async def feedback(self,ctx,q):
        embed = discord.Embed(title="BUG回報",description=f"回報者:{ctx.author}\n問題:{q}")
        channel = self.bot.get_channel(1079959297133400114)
        await channel.send(embed=embed)
        await ctx.respond("回報成功,感謝您的回報!!!")
            



def setup(bot):
    bot.add_cog(ticket(bot))
