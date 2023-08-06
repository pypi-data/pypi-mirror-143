# ditolo

<a href="https://pypi.python.org/pypi/ditolo">
<img src="https://img.shields.io/pypi/v/py-cord.svg"></img>
</a>
<a alt="PyPI downloads" href="https://pypi.python.org/pypi/ditolo"><img src="https://img.shields.io/pypi/dm/ditolo?color=blue"></a>

**discord token login extension packege**

# example code!!!
```
import ditolo
from ditolo import *

ditolo.join("アカウントのトークンbotではない","inviteリンク")
ditolo.join(token="アカウントのトークンbotではない",link="inviteリンク")

ditolo.send("アカウントのトークンbotではない","チャンネルid","送信するメッセージ")
ditolo.send(token="アカウントのトークンbotではない",channel="チャンネルid",content="送信するメッセージ")


ditolo.leave(アカウントのトークンbotではない,"サーバーid","trueかfalse")
ditolo.leave(token="アカウントのトークンbotではない",guild_id="サーバーid",print="trueかfalse")


ditolo.check("アカウントのトークンbotではない","trueかfalse")
ditolo.check(token="アカウントのトークンbotではない",print="trueかfalse")
```
