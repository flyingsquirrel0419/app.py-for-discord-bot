import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# -------------------------
# .env 로드
# -------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN 이 .env 에 존재하지 않습니다.")

# -------------------------
# Intents
# -------------------------
intents = discord.Intents.default()
intents.message_content = True

# -------------------------
# Bot 클래스
# -------------------------
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        # cogs 자동 로딩
        await self.load_all_cogs()

        # 슬래시 / 하이브리드 명령어 동기화
        synced = await self.tree.sync()
        print(f"[SYNC] 슬래시 명령어 {len(synced)}개 동기화 완료")

    async def load_all_cogs(self):
        if not os.path.isdir("./cogs"):
            print("[WARN] cogs 폴더가 없습니다.")
            return

        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                ext = f"cogs.{file[:-3]}"
                try:
                    await self.load_extension(ext)
                    print(f"[LOAD] {ext}")
                except Exception as e:
                    print(f"[ERROR] {ext} 로드 실패: {e}")

# -------------------------
# Bot 인스턴스
# -------------------------
bot = MyBot()

# -------------------------
# Cog 리로드 명령어
# -------------------------
@bot.command(name="sys_reload")
@commands.is_owner()
async def sys_reload(ctx, cog_name: str):
    """
    사용법: !sys_reload attendance
    """
    ext = f"cogs.{cog_name}"

    try:
        await bot.reload_extension(ext)
        await bot.tree.sync()
        await ctx.send(f"✅ `{ext}` 리로드 완료 (슬래시 명령어 재동기화)")
    except commands.ExtensionNotFound:
        await ctx.send("❌ 해당 Cog 파일을 찾을 수 없습니다.")
    except commands.ExtensionNotLoaded:
        await ctx.send("❌ 해당 Cog 는 로드되어 있지 않습니다.")
    except Exception as e:
        await ctx.send(f"❌ 오류 발생\n```{e}```")

# -------------------------
# Bot 실행
# -------------------------
bot.run(TOKEN)
