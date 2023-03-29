import discord
import json
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command


class set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="查看目前群組設置")
    async def setting(self, ctx):
        await ctx.defer()

        path = F"database/guild.json"
        with open(path, "r") as file:
            data = json.load(file)

            try:
                channel = await ctx.guild.fetch_channel(
                    data[str(ctx.guild.id)]["set"]["channel"])
                role = ctx.guild.get_role(
                    data[str(ctx.guild.id)]["set"]["role"])
            except:
                embed = discord.Embed(
                    title="錯誤", description="找不到身分組或頻道,請管理員重新設置")
                await ctx.respond(embed=embed)
                return

        embed = discord.Embed(title="群組設置")
        embed.add_field(name="頻道", value=F"> {channel.mention}")
        embed.add_field(name="管理", value=F"> {role.mention}")
        await ctx.respond(embed=embed)

    @slash_command(description="在群組設置合作")
    async def set(self, ctx,
                  channel: Option(discord.TextChannel, "通知訊息頻道"),
                  role: Option(discord.Role, "管理合作事務身分組")):
        await ctx.defer()  # 延遲回應

        # 檢測是否為管理員
        if not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title="權限不足", description="只有管理員能使用此指令")
            await ctx.respond(embed=embed)
            return

        # 開啟資料檔案
        path = "database/guild.json"
        with open(path, "r") as file:
            data = json.load(file)

            # 檢查是該群是否有字典,否則創建
            if not str(ctx.guild.id) in data.keys():
                data[str(ctx.guild.id)] = {}

            # 寫入字典資訊
            data[str(ctx.guild.id)]["set"] = {
                "channel": channel.id, "role": role.id}
            data[str(ctx.guild.id)]["partners"] = []

        # 上傳資料
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
        embed = discord.Embed(title="群組設置更新")
        embed.add_field(name="頻道", value=F"> {channel.mention}")
        embed.add_field(name="管理", value=F"> {role.mention}")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(set(bot))
