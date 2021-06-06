"use strict";

function Random(seed) {
    this._seed = Math.round(seed) % 2147483647;
    if (this._seed <= 0) this._seed += 2147483646;

    this.randInt = function () {
        return this._seed = this._seed * 16807 % 2147483647;
    };
    this.randFloat = function () {
        return (this.randInt() - 1) / 2147483646;
    };
    this.randBit = function () {
        return (this.randInt() >> 15) & 1;
    };
    this.randBinaryString = function (n) {
        var s = "";
        for (var i = 0; i < n; i++) s += String(this.randBit());
        return s;
    };
};

function BitBuffer(str) {
    this.length = str.length;
    this.arr = [];
    for (var i = 0; i < this.length; i++) {
        this.arr.push(str.charCodeAt(i) % 2);
    }
    this.index = 0;

    this.nextBit = function () {
        var ans = this.arr[this.index];
        this.index = (this.index + 1) % this.length;
        return ans;
    };
    this.nextInt = function (bitcount) {
        var x = 0;
        for (var i = 0; i < bitcount; i++) {
            x = (x << 1) + this.nextBit();
        }
        return x;
    };
    this.nextFloat = function (bitcount) {
        return this.nextInt(bitcount) / (1 << bitcount);  // [0,1)
    };
}


function IdenticonGithub(bitBuffer) {

    // generate blocks (15 bit)
    var blocks = [];
    const TILES = 5;
    for (var j = 0; j < TILES; j++) {
        for (var i = 0; i < Math.floor(TILES / 2); i++) {
            if (bitBuffer.nextBit()) {
                blocks.push([i / TILES, j / TILES]);
                blocks.push([(TILES - i - 1) / TILES, j / TILES]);
            }
        }
        if (TILES % 2 == 1 && bitBuffer.nextBit()) {
            blocks.push([Math.floor(TILES / 2) / TILES, j / TILES]);
        }
    }
    this.blockSize = 1.0 / TILES;
    this.blocks = blocks;

    // generate colors (24 bit)
    var hue = 360.0 * bitBuffer.nextFloat(8);
    var sat = 0.45 + 0.20 * bitBuffer.nextFloat(8);
    var bri = 0.55 + 0.20 * bitBuffer.nextFloat(8);
    this.color = "hsl(" + [hue, 100 * sat + '%', 100 * bri + '%'].join(',') + ")";

    // drawing
    this.renderCanvas = function (canvas, x, y, w, h) {
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "#f0f0f0";
        ctx.fillRect(x, y, w, h);
        ctx.fillStyle = this.color;
        for (var i = 0; i < this.blocks.length; i++) {
            const pad = 1.0 / 12.0, wid = 1.0 - 2 * pad;
            const aa_offset = 0.5;
            ctx.fillRect(
                x + (pad + wid * this.blocks[i][0]) * w - aa_offset,
                y + (pad + wid * this.blocks[i][1]) * h - aa_offset,
                wid * this.blockSize * w + 2 * aa_offset,
                wid * this.blockSize * h + 2 * aa_offset
            );
        }
    };
}
