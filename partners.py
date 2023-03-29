import discord
import json
from discord.ext import commands
from discord.commands import slash_command


class Ann(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label="公告內容", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        # 開啟資料檔案
        path = "database/guild.json"
        with open(path, "r") as file:
            data = json.load(file)

        # 公告embed
        ann = discord.Embed(
            title="合作群公告",
            description=F"\
                由**`{interaction.guild}`** **`{interaction.user}`**發出的合作公告\
                \n```\n{self.children[0].value}\n```")

        # 找尋所有合作群組
        txt = ""
        for partner in data[str(interaction.guild.id)]["partners"]:
            # 尋找群組
            try:
                guild = await interaction.client.fetch_guild(partner)
            except:
                txt += F"> `{partner}` 找不到群組\n\n"
            else:
                # 尋找頻道
                try:
                    channel = await guild.fetch_channel(data[str(guild.id)]["set"]["channel"])
                except:
                    txt += F"> `{guild}` 找不到群組頻道\n\n"
                # 傳送訊息
                else:
                    try:
                        await channel.send(embed=ann)
                        txt += F"> `{guild}` 成功傳送公告\n\n"
                    except:
                        txt += F"> `{guild}` 無法傳送訊息\n\n"

        embed = discord.Embed(
            title="已發布群組公告",
            description=txt
        )
        await interaction.response.send_message(embed=embed)


class partners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="查看當前所有合作",guild_ids=[1079954205286092862])
    async def partners(self, ctx):
        await ctx.defer()

        # 開啟檔案
        path = "database/guild.json"
        with open(path, "r") as file:
            data = json.load(file)

        # 檢測群組是否有設置
        if not str(ctx.guild.id) in data.keys():
            embed = discord.Embed(
                title="本群沒有設置",
                description="""若要使用本服務
                請先讓管理員使用**`/set`**指令""")
            await ctx.respond(embed=embed)
            return

        # 列出合作夥伴
        txt = ""
        for partner in data[str(ctx.guild.id)]["partners"]:
            try:
                guild = await self.bot.fetch_guild(partner)
            except:
                txt += F"> `{partner}` 找不到群組\n\n"
            else:
                txt += F"> {guild}\n> `{guild.id}`\n\n"
        embed = discord.Embed(
            title="所有合作群組",
            description=txt)
        await ctx.respond(embed=embed)

    @slash_command(description="在所有合作群發出公告")
    async def parann(self, ctx):

        # 開啟資料檔案
        path = "database/guild.json"
        with open(path, "r") as file:
            data = json.load(file)

        # 檢查是否有正確設置
        try:
            channel = await ctx.guild.fetch_channel(data[str(ctx.guild.id)]["set"]["channel"])
            role = ctx.guild.get_role(data[str(ctx.guild.id)]["set"]["role"])
        except:
            embed = discord.Embed(
                title="錯誤",
                description=F"""
                找不到本群設置的頻道或身分組
                請管理員重新設置
                """)

        # 檢查是否為合作管理員發出
        if not role in ctx.author.roles:
            embed = discord.Embed(
                title="權限不足", description=F"只有{role.mention}能使用此指令")
            await ctx.respond(embed=embed)
            return

        # 發送對話框
        modal = Ann(title="對所有合作群傳送公告")
        await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(partners(bot))
