"""This module is for the translation mapping data of the
following document:

Document file: animation_reverse.md
Language: jp
"""

from typing import Dict

MAPPING: Dict[str, str] = {

    '# animation_reverse interface':
    '# animation_reverse インターフェイス',

    'This page explains the `animation_reverse` method interface.':
    'このページでは`animation_reverse`メソッドのインターフェイスについて説明します。',

    '## What interface is this?':
    '## インターフェイス概要',

    'The `animation_reverse` interface reverses the running animations.':
    '`animation_reverse`インターフェイスは動いているアニメーションの再生を反転（逆再生）します。',

    'This interface exists in the instances that have the animation interfaces (such as the `animation_x`\\, `animation_move`).':  # noqa
    'このインターフェイスは`animation_x`や`animation_move`などのアニメーション関係のインターフェイスを持つクラスのインスタンス上に存在します。',  # noqa

    '## Basic usage':
    '## 使い方例',

    'The following example sets the x-coordinate animation and starts the 1-second interval timer to reverse animation with the `animation_reverse` interface.':  # noqa
    '以下の例ではX座標のアニメーションを設定し、1秒ごとの間隔で`animation_reverse`インターフェイスを使ってアニメーションを反転（逆作成）しています。',  # noqa

    '```py\n# runnable\nfrom typing_extensions import TypedDict\n\nimport apysc as ap\n\n\nclass _RectOptions(TypedDict):\n    rectangle: ap.Rectangle\n\n\ndef on_timer_1(e: ap.TimerEvent, options: _RectOptions) -> None:\n    """\n    The event handler that timer calls after the 3 seconds.\n\n    Parameters\n    ----------\n    e : ap.TimerEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    ap.Timer(on_timer_2, delay=1000, options=options).start()\n\n\ndef on_timer_2(e: ap.TimerEvent, options: _RectOptions) -> None:\n    """\n    The event handler that timer calls every second.\n\n    Parameters\n    ----------\n    e : ap.TimerEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    rectangle: ap.Rectangle = options[\'rectangle\']\n    rectangle.animation_reverse()\n\n\nap.Stage(\n    stage_width=500, stage_height=150, background_color=\'#333\',\n    stage_elem_id=\'stage\')\nsprite: ap.Sprite = ap.Sprite()\nsprite.graphics.begin_fill(color=\'#0af\')\n\nrectangle: ap.Rectangle = sprite.graphics.draw_rect(\n    x=50, y=50, width=50, height=50)\nrectangle.animation_x(x=400, duration=5000).start()\noptions: _RectOptions = {\'rectangle\': rectangle}\nap.Timer(\n    on_timer_1, delay=3000, repeat_count=1,\n    options=options).start()\n\nap.save_overall_html(\n    dest_dir_path=\'animation_reverse_basic_usage/\')\n```':  # noqa
    '```py\n# runnable\nfrom typing_extensions import TypedDict\n\nimport apysc as ap\n\n\nclass _RectOptions(TypedDict):\n    rectangle: ap.Rectangle\n\n\ndef on_timer_1(e: ap.TimerEvent, options: _RectOptions) -> None:\n    """\n    The event handler that timer calls after the 3 seconds.\n\n    Parameters\n    ----------\n    e : ap.TimerEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    ap.Timer(on_timer_2, delay=1000, options=options).start()\n\n\ndef on_timer_2(e: ap.TimerEvent, options: _RectOptions) -> None:\n    """\n    The event handler that timer calls every second.\n\n    Parameters\n    ----------\n    e : ap.TimerEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    rectangle: ap.Rectangle = options[\'rectangle\']\n    rectangle.animation_reverse()\n\n\nap.Stage(\n    stage_width=500, stage_height=150, background_color=\'#333\',\n    stage_elem_id=\'stage\')\nsprite: ap.Sprite = ap.Sprite()\nsprite.graphics.begin_fill(color=\'#0af\')\n\nrectangle: ap.Rectangle = sprite.graphics.draw_rect(\n    x=50, y=50, width=50, height=50)\nrectangle.animation_x(x=400, duration=5000).start()\noptions: _RectOptions = {\'rectangle\': rectangle}\nap.Timer(\n    on_timer_1, delay=3000, repeat_count=1,\n    options=options).start()\n\nap.save_overall_html(\n    dest_dir_path=\'animation_reverse_basic_usage/\')\n```',  # noqa

    '## Interface Notes':
    '## インターフェイスの特記事項',

    'This interface can only use during animation. If you use this at the end of the animation, nothing happens, as follows:':  # noqa
    'このインターフェイスはアニメーションが動いている間のみ使用することができます。以下のコード例のようにアニメーションが終了している状態で呼び出しても何も発生せずアニメーションが終了した状態のままとなります:',  # noqa

    '```py\n# runnable\nfrom typing_extensions import TypedDict\n\nimport apysc as ap\n\n\nclass _RectOptions(TypedDict):\n    rectangle: ap.Rectangle\n\n\ndef on_timer(e: ap.TimerEvent, options: _RectOptions) -> None:\n    """\n    The handler that the timer calls.\n\n    Parameters\n    ----------\n    e : ap.TimerEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    rectangle: ap.Rectangle = options[\'rectangle\']\n\n    # Nothing happens since the animation has already been completed.\n    rectangle.animation_reverse()\n\n\nap.Stage(\n    stage_width=500, stage_height=150, background_color=\'#333\',\n    stage_elem_id=\'stage\')\nsprite: ap.Sprite = ap.Sprite()\nsprite.graphics.begin_fill(color=\'#0af\')\n\nrectangle: ap.Rectangle = sprite.graphics.draw_rect(\n    x=50, y=50, width=50, height=50)\nrectangle.animation_x(x=400, duration=1000).start()\n\noptions: _RectOptions = {\'rectangle\': rectangle}\nap.Timer(on_timer, delay=1500, repeat_count=1, options=options).start()\n\nap.save_overall_html(\n    dest_dir_path=\'animation_reverse_notes/\')\n```':  # noqa
    '```py\n# runnable\nfrom typing_extensions import TypedDict\n\nimport apysc as ap\n\n\nclass _RectOptions(TypedDict):\n    rectangle: ap.Rectangle\n\n\ndef on_timer(e: ap.TimerEvent, options: _RectOptions) -> None:\n    """\n    The handler that the timer calls.\n\n    Parameters\n    ----------\n    e : ap.TimerEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    rectangle: ap.Rectangle = options[\'rectangle\']\n\n    # Nothing happens since the animation has already been completed.\n    rectangle.animation_reverse()\n\n\nap.Stage(\n    stage_width=500, stage_height=150, background_color=\'#333\',\n    stage_elem_id=\'stage\')\nsprite: ap.Sprite = ap.Sprite()\nsprite.graphics.begin_fill(color=\'#0af\')\n\nrectangle: ap.Rectangle = sprite.graphics.draw_rect(\n    x=50, y=50, width=50, height=50)\nrectangle.animation_x(x=400, duration=1000).start()\n\noptions: _RectOptions = {\'rectangle\': rectangle}\nap.Timer(on_timer, delay=1500, repeat_count=1, options=options).start()\n\nap.save_overall_html(\n    dest_dir_path=\'animation_reverse_notes/\')\n```',  # noqa

    '## animation_reverse API':
    '## animation_reverse API',

    '<span class="inconspicuous-txt">Note: the document build script generates and updates this API document section automatically. Maybe this section is duplicated compared with previous sections.</span>':  # noqa
    '<span class="inconspicuous-txt">特記事項: このAPIドキュメントはドキュメントビルド用のスクリプトによって自動で生成・同期されています。そのためもしかしたらこの節の内容は前節までの内容と重複している場合があります。</span>',  # noqa

    '**[Interface summary]** Reverse all running animations.<hr>':
    '**[インターフェイス概要]** 動いている全てのアニメーションを反転（逆再生）します。<hr>',

    '**[Notes]**':
    '**[特記事項]**',

    'Suppose you call this interface multiple times and animations reach the beginning or end of the animation. In that case, this interface ignores the reverse instruction. This behavior means that the same interval\'s timer tick reverse setting does not work correctly (since the same interval setting reaches the animation start).<hr>':  # noqa
    '複数回このインターフェイスを呼び出した際などに、アニメーションの最初もしくは最後に到達しアニメーションが停止した場合、その後にこのインターフェイスを呼び出しても反転（逆再生）はされずに停止したままとなります。そのためアニメーション時間と同じ時間のタイマーなどで反転の指定した場合などは正常に動作しません。<hr>',  # noqa

    '**[Examples]**':
    '**[コードサンプル]**',

    '```py\n>>> from typing_extensions import TypedDict\n>>> import apysc as ap\n>>> class RectOptions(TypedDict):\n...     rectangle: ap.Rectangle\n>>> def on_timer(\n...         e: ap.TimerEvent,\n...         options: RectOptions) -> None:\n...     rectangle: ap.Rectangle = options[\'rectangle\']\n...     rectangle.animation_reverse()\n>>> stage: ap.Stage = ap.Stage()\n>>> sprite: ap.Sprite = ap.Sprite()\n>>> sprite.graphics.begin_fill(color=\'#0af\')\n>>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(\n...     x=50, y=50, width=50, height=50)\n>>> _ = rectangle.animation_x(\n...     x=100,\n...     duration=1500,\n...     easing=ap.Easing.EASE_OUT_QUINT,\n... ).start()\n>>> options: RectOptions = {\'rectangle\': rectangle}\n>>> ap.Timer(on_timer, delay=750, options=options).start()\n```':  # noqa
    '```py\n>>> from typing_extensions import TypedDict\n>>> import apysc as ap\n>>> class RectOptions(TypedDict):\n...     rectangle: ap.Rectangle\n>>> def on_timer(\n...         e: ap.TimerEvent,\n...         options: RectOptions) -> None:\n...     rectangle: ap.Rectangle = options[\'rectangle\']\n...     rectangle.animation_reverse()\n>>> stage: ap.Stage = ap.Stage()\n>>> sprite: ap.Sprite = ap.Sprite()\n>>> sprite.graphics.begin_fill(color=\'#0af\')\n>>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(\n...     x=50, y=50, width=50, height=50)\n>>> _ = rectangle.animation_x(\n...     x=100,\n...     duration=1500,\n...     easing=ap.Easing.EASE_OUT_QUINT,\n... ).start()\n>>> options: RectOptions = {\'rectangle\': rectangle}\n>>> ap.Timer(on_timer, delay=750, options=options).start()\n```',  # noqa

}
