#!/usr/bin/env -S v run 

import vweb

struct App {
    vweb.Context
}

@['/']
fn (mut app App) world() vweb.Result {
    return app.text('Hello, world!\n')
}

fn main() {
    vweb.run(&App{}, 8000)
}