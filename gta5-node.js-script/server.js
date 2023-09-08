const { uIOhook, UiohookKey } = require('uiohook-napi');

// const keypress = require('keypress');

// keypress(process.stdin);

// process.stdin.on('keypress', (ch, key) => {
//   console.log('got "keypress"', key);
//   if (key && key.ctrl && key.name === 'c') {
//     process.stdin.pause(); // 停止命令行输入
//   }
// });

// process.stdin.resume(); // 开始命令行输入

uIOhook.on('keydown', (e) => {
  if (e.keycode === UiohookKey.Q) {
    console.log('Hello!');
  }

  if (e.keycode === UiohookKey.Escape) {
    process.exit(0);
  }
});

uIOhook.start();
