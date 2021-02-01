import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from .util import random_image, SPONGEBOB_CHICKEN_DIR


class SpongebobChickenJoke(Joke):
    def __init__(self):
        """InIt FoR tHe SpOnGeBoB cHicKeN jOkE.

        ThE jOkE iS tO sImPlY pArRoT tHe MeSsAgE bAcK bUt WiTh "ChIcKeN CaSe"
        aPpLiEd. AdDiTiOnLy a GiF oF SpOnGeBob As A ChIcKeN iS SeNt. AlL oF
        tHiS iS tO mOcK tHe MeSsAgE sEnT.
        """
        # Set up super class
        super().__init__("SpOnGeBoB_cHicKeN", 1)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """ReTuRn SuCcEsS aS tO sEnDiNg A sTiCkBuG gIf.

        PaRaMeTeRs
        ----------
        bot: Red
            ThE rEdBoT eXeCuTiNg ThIs FuNcTiOn.
        msg: discord.Message
            MeSsaGe To aTtEmPt A jOkE uPoN

        ReTuRnS
        -------
        bool
            SuCcEsS oF jOkE.
        """
        # ChEcK tHeRe Is AcTuAlLy TeXt In ThE mEsSaGe
        if len(msg.content) == 0:
            return False
        # LoG jOkE
        self.log_info(msg.guild, msg.author, "GoTeM")
        # ConStRuCt oUr ReSpOnSe
        response = {"description":self.chicken_case(msg.content)}
        # PiCk RaNdOm GiF
        spongebob_gif = random_image(SPONGEBOB_CHICKEN_DIR)
        # CoNsTrUcT eMbEd
        embed = discord.Embed.from_dict(response)
        embed.set_image(url=f"attachment://{spongebob_gif.filename}")
        # SeNd EmBeD aNd sPoNgEbOb cHiCkEn GiF
        await msg.channel.send(embed=embed, file=spongebob_gif)
        # ReTuRn SuCcSeSs
        return True


    @classmethod
    def chicken_case(cls, string:str):
        """ReTuRnS sTrInG iN cHiCkEn CaSe

        PaRaMeTeRs
        ----------
        string:str
            ThE sTrInG tO aPpLy ChIcKeN cAsE to

        ReTuRnS
        -------
        str
            ThE sTrInG iN ChIcKeN CaSe
        """
        def helper():
            # It'S eAsIeR tO dO tHiS vIa aN iTeRaToR
            upper=True
            for character in string:
                if character.isalpha():
                    if upper:
                        yield character.upper()
                    else:
                        yield character.lower()
                    upper = not upper
                else:
                    yield character
        # TuRn ThE iTeRaToRaToR iNtO a StRiNg
        return "".join(helper())
        
