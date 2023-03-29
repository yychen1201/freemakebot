import discord
import json
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command


# 一個無法按的按鈕
class Null(discord.ui.View):
    @discord.ui.button(label="https://www.dcadminbot.cf/", style=discord.ButtonStyle.green, disabled=True)
    async def null_button_callback(self, button, interaction):
        pass    


class Invite(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="接受邀請", custom_id="accept", row=0, style=discord.ButtonStyle.green)
    async def accept_button_callback(self, button, interaction):

        # 抓取對方群組
        try:
            guild = await interaction.client.fetch_guild(int(interaction.message.content))
        except:
            embed = discord.Embed(
                title="錯誤", description="找不到群組,可能是該群組不繼續使用本服務了")
            await interaction.response.send_message(embed=embed)
            return

        path = "database/guild.json"
        with open(path, "r") as file:
            data = json.load(file)

            # 檢查是否為合作管理員發出
            role = interaction.guild.get_role(
                data[str(interaction.guild.id)]["set"]["role"])
            if not role in interaction.user.roles:
                embed = discord.Embed(
                    title="權限不足", description=F"只有{role.mention}能使用")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # 檢查是否已合作
            if guild.id in data[str(interaction.guild.id)]["partners"]:
                embed = discord.Embed(title="本群已和該群組已建立合作關係")
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=3)
                return

            # 新增串列資料中的合作群組項
            data[str(interaction.guild.id)]["partners"].append(guild.id)
            data[str(guild.id)]["partners"].append(interaction.guild.id)

            # 回傳接受訊息給原群組
            try:
                channel = await interaction.client.fetch_channel(data[str(guild.id)]["set"]["channel"])
                embed = discord.Embed(
                    title="合作成功",
                    description=F"""
                    **`{interaction.guild}`**
                    的邀請已被對方接受
                    已成功建立合作關係
                    """)
                await channel.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="錯誤",
                    description=F"""
                    對方的合作頻道可能已被刪除
                    或是在對方的群組機器人沒權限
                    請先請對方確認
                    """)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        # 編輯原訊息
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
        embed = discord.Embed(
            title="合作邀請",
            description=F"""
            {interaction.user.mention} 已接受
            來自 {guild} 的合作邀請
            """)
        await interaction.message.edit(embed=embed, view=Null())

        await interaction.response.defer()

    @discord.ui.button(label="拒絕邀請", custom_id="reject", row=1, style=discord.ButtonStyle.red)
    async def reject_button_callback(self, button, interaction):

        # 抓取該群組資訊
        try:
            guild = await interaction.client.fetch_guild(int(interaction.message.content))
        except:
            embed = discord.Embed(
                title="錯誤", description="找不到群組,可能是該群組不繼續使用本服務了")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        with open("database/guild.json", "r") as file:
            data = json.load(file)

            # 檢查是否為合作管理員發出
            role = interaction.guild.get_role(
                data[str(interaction.guild.id)]["set"]["role"])
            if not role in interaction.user.roles:
                embed = discord.Embed(
                    title="權限不足", description=F"只有{role.mention}能使用")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # 檢查是否已合作
            if guild.id in data[str(interaction.guild.id)]["partners"]:
                embed = discord.Embed(
                    title="本群已和該群組已建立合作關係",
                    description=F"""
                    如要解除合作
                    請使用指令**`/lifted`**
                    """)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        # 編輯原訊息
        embed = discord.Embed(
            title="已拒絕邀請",
            description=F"""
            {interaction.user.mention}殘忍拒絕了**`{guild}`**的合作邀請
            """)
        await interaction.message.edit(embed=embed, view=Null())

        # 回傳拒絕訊息給原群組
        try:
            channel = await interaction.client.fetch_channel(data[str(guild.id)]["set"]["channel"])
            embed = discord.Embed(
                title="合作失敗",
                description=F"""
                **`{interaction.guild}`**
                的邀請被對方拒絕
                """)
            await channel.send(embed=embed)
        except:
            embed = discord.Embed(
                title="錯誤",
                description=F"""無法傳送拒絕訊息至對方群組""")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.defer()


class patner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 啟動舊按鈕
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Invite())

    @slash_command(description="邀請群組合作",guild_ids=[1079954205286092862])
    async def invite(self, ctx, guild: Option(discord.Guild, "要邀請的群組ID")):
        await ctx.defer()  # 延遲反應

        # 開啟檔案
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
            await ctx.respond(embed=embed)
            return

        # 檢查是否為合作管理員發出
        if not role in ctx.author.roles:
            embed = discord.Embed(
                title="權限不足", description=F"只有{role.mention}能使用此指令")
            await ctx.respond(embed=embed)
            return

        # 檢測該群是否有資訊
        if not str(guild.id) in data.keys():
            embed = discord.Embed(
                title="錯誤",
                description="""
            可能是該群組沒有使用過/set指令
            請對方再檢查一下八
            """)
            await ctx.respond(embed=embed)
            return

        # 檢測是否已合作
        if guild.id in data[str(ctx.guild.id)]["partners"]:
            embed = discord.Embed(title="本群已和該群組已建立合作關係")
            await ctx.respond(embed=embed)
            return

        with open("database/ban.json","r") as bans:
            bans = json.load(bans)
            if ctx.guild.id in bans:
                return await ctx.respond("本群組已被禁止使用本服務")

        # 抓取頻道並檢測頻道是否存在
        try:
            channel = await guild.fetch_channel(data[str(guild.id)]["set"]["channel"])
        except:
            embed = discord.Embed(
                title="錯誤",
                description=F"""
                找不該群設置的頻道
                請對方檢查並重新設置
                """)
            await ctx.respond(embed=embed)
            return

        # 傳送合作邀請
        embed = discord.Embed(
            title="合作邀請",
            description=F"""
            您的群組收到了來自**`{ctx.guild.name}`**的合作邀請
            這通常是在您和對方有連繫後的結果
            """)
        await channel.send(content=ctx.guild.id, embed=embed, view=Invite())

        # 反應成功指令
        embed = discord.Embed(title=F"已發送邀請至{guild}")
        await ctx.respond(embed=embed)

    @slash_command(description="解除合作",guild_ids=[1079954205286092862])
    async def lifted(self, ctx,
                     guild: Option(str, "要解除合作的群組"),
                     reason: Option(str, "解除合作原因", default="無原因")):
        await ctx.defer()

        try:
            guild = int(guild)
        except:
            embed=discord.Embed(title="錯誤",description="請輸入正確的ID")
            await ctx.respond(embed=embed)
            return

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

        # 檢查是否已合作
        if not guild in data[str(ctx.guild.id)]["partners"]:
            embed = discord.Embed(
                title="錯誤",
                description=F"""
                本群和該群沒有建立過合作關係
                """)
            await ctx.respond(embed=embed)
            return

        # 搜尋該群頻道
        try:
            Guild = await self.bot.fetch_guild(guild)
            channel = await Guild.fetch_channel(data[str(Guild.id)]["set"]["channel"])
            embed = discord.Embed(
                title="合作解除通知",
                description=F"""
                {ctx.guild} 解除了和您的合作
                原因: `{reason}`
                """)
            await channel.send(embed=embed)
        except:
            pass

        # 修改字典資訊
        data[str(ctx.guild.id)]["partners"].remove(guild)
        data[str(guild)]["partners"].remove(ctx.guild.id)

        # 上傳資料
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

        # 傳送回應
        embed = discord.Embed(
            title="解除合作",
            description=F"已解除與**`{guild}`**的合作")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(patner(bot))
