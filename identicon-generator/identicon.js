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


// 32 bits
function IdenticonGithub(bitBuffer) {

    // generate blocks (15 bits)
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

    // generate colors (17 bits)
    var hue = 360.0 * bitBuffer.nextFloat(7);
    var sat = 0.45 + 0.20 * bitBuffer.nextFloat(5);
    var bri = 0.55 + 0.20 * bitBuffer.nextFloat(5);
    this.color = "hsl(" + [hue, 100 * sat + '%', 100 * bri + '%'].join(',') + ")";

    // drawing
    this.renderCanvas = function (canvas, x, y, w, h) {
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "#f0f0f0";
        ctx.fillRect(x, y, w, h);
        ctx.fillStyle = this.color;
        for (var i = 0; i < this.blocks.length; i++) {
            const pad = 1.0 / 12.0, wid = 1.0 - 2 * pad;
            const aa_offset = 0.0;  // or 0.5 to avoid anti-aliasing effect
            ctx.fillRect(
                x + (pad + wid * this.blocks[i][0]) * w - aa_offset,
                y + (pad + wid * this.blocks[i][1]) * h - aa_offset,
                wid * this.blockSize * w + 2 * aa_offset,
                wid * this.blockSize * h + 2 * aa_offset
            );
        }
    };
}


// 62 bits
function IdenticonGravatar(bitBuffer) {

    // primitive tiles, clockwise in screen coordinate
    // https://barro.github.io/2018/02/avatars-identicons-and-hash-visualization/
    const tiles = [
        // 0-10
        [[0, 0, 1, 0, 1, 0.5, 0, 0.5]],
        [[0, 0, 1, 0, 1, 1, 0, 1]],
        [[0, 0, 1, 0, 0, 1]],
        [[0, 0.5, 1, 0, 1, 1]],
        [[0.5, 0, 1, 0.5, 0.5, 1, 0, 0.5]],
        [[0, 0, 1, 0.5, 1, 1, 0.5, 1]],
        [[0, 0.5, 0.5, 0.25, 0.5, 0.75], [0.5, 0.25, 1, 0, 1, 0.5], [0.5, 0.75, 1, 0.5, 1, 1]],
        [[0, 0, 1, 0.5, 0.5, 1]],
        [[0.25, 0.25, 0.75, 0.25, 0.75, 0.75, 0.25, 0.75]],
        [[0, 0.5, 0.5, 0.5, 0, 1], [0.5, 0, 1, 0, 0.5, 0.5]],
        [[0, 0, 0.5, 0, 0.5, 0.5, 0, 0.5]],
        // 11-21
        [[0.5, 0, 1, 0.5, 0.5, 1]],
        [[1, 0, 1, 1, 0.5, 0.5]],
        [[0.5, 0, 0.5, 0.5, 0, 0.5]],
        [[0, 0, 0.5, 0, 0, 0.5]],
        [[0, 0, 0.5, 0, 0.5, 0.5, 0, 0.5], [0.5, 0.5, 1, 0.5, 1, 1, 0.5, 1]],
        [[0, 0, 0.5, 0.5, 0, 1], [0.5, 0.5, 1, 0, 1, 1]],
        [[0, 0, 1, 0, 0, 0.5]],
        [[0, 0, 1, 0, 0, 0.5], [0, 0.5, 1, 0.5, 0, 1]],
        [[0, 0, 1, 0, 0, 0.5], [0, 0.5, 0.5, 0.5, 0, 1]],
        [[0, 0, 1, 0.5, 1, 1]],
        [[0.5, 0, 1, 0, 0.5, 0.5], [0, 0.5, 0.5, 0.5, 0, 1], [0.5, 0.5, 1, 0.5, 0.5, 1]],
        // 22-32
        [[0.5, 0.25, 1, 0, 1, 0.5], [0.5, 0.75, 1, 0.5, 1, 1]],
        [[0, 0, 1, 0, 0.5, 0.25], [0, 1, 0.5, 0.75, 1, 1]],
        [[0, 0, 1, 0, 0.5, 0.25], [0, 1, 0.5, 0.75, 1, 1], [0, 0.5, 0.5, 0.25, 1, 0.5, 0.5, 0.75]],
        [[0.5, 0.25, 0.75, 0.5, 0.5, 0.75, 0.25, 0.5]],
        [[0, 0, 1, 0, 0.5, 0.25], [1, 0, 1, 1, 0.75, 0.5], [1, 1, 0, 1, 0.5, 0.75], [0, 1, 0, 0, 0.25, 0.5]],
        [[0, 0.5, 0.5, 0, 0.5, 1], [0.5, 0.5, 1, 0, 1, 1]],
        [[0, 0, 1, 0.5, 1, 1], [0, 0.5, 1, 0, 0, 1]],
        [[0, 0, 1, 0, 0, 0.5], [0, 1, 1, 0.5, 1, 1]],
        [[0, 0, 1, 0, 0.5, 0.25], [1, 0, 1, 1, 0.75, 0.5], [1, 1, 0, 1, 0.5, 0.75], [0, 1, 0, 0, 0.25, 0.5], [0.25, 0.5, 0.5, 0.25, 0.75, 0.5, 0.5, 0.75]],
        [[0.5, 1, 0, 0.5, 0.25, 0.5, 0.5, 0.75], [0, 0.5, 0.5, 0, 0.5, 0.25, 0.25, 0.5], [0.5, 0, 1, 0.5, 0.75, 0.5, 0.5, 0.25]],
        [[0, 0.5, 0.5, 0.25, 1, 0.5, 0.5, 0.75]],
        // 33-43
        [[0, 0, 0.5, 0, 0, 0.5], [0.5, 0, 1, 0, 0.5, 0.5], [0, 0.5, 0.5, 0.5, 0, 1], [0.5, 0.5, 1, 0.5, 0.5, 1]],
        [[0.5, 1, 0, 0.5, 0.25, 0.5, 0.5, 0.75], [0, 0.5, 0.5, 0, 0.5, 0.25, 0.25, 0.5], [0.5, 0, 1, 0.5, 0.75, 0.5, 0.5, 0.25], [1, 0.5, 0.5, 1, 0.5, 0.75, 0.75, 0.5]],
        [[0, 0.5, 0.5, 0.75, 0, 1], [0.5, 0.25, 1, 0, 1, 0.5], [0.75, 0.5, 1, 1, 0.5, 1]],
        [[0, 0.5, 0.5, 0.75, 0, 1], [0.75, 0.5, 1, 1, 0.5, 1]],
        [[0, 0.5, 0.5, 0.75, 0, 1], [0.5, 0.25, 1, 0, 1, 0.5]],
        [[0, 0.5, 1, 0, 0.5, 0.5], [0, 0.5, 0.5, 0.5, 1, 1]],
        [[0, 0.5, 1, 0, 0.5, 0.5], [0, 0.5, 0.5, 0.5, 1, 1], [0.75, 0.25, 1, 0, 1, 1, 0.75, 0.75]],
        [[0, 0, 0.5, 0, 0, 0.5], [0.5, 1, 1, 0.5, 1, 1]],
        [[0, 0, 0.5, 0, 0.5, 0.25, 0, 0.5], [0.5, 0.75, 1, 0.5, 1, 1, 0.5, 1]],
        [[0.5, 0, 0.75, 0.25, 0.5, 0.5, 0.25, 0.25], [0.5, 0.5, 0.75, 0.75, 0.5, 1, 0.25, 0.75]],
        [[0.5, 0, 1, 0, 0.5, 0.5, 0.25, 0.25], [0.5, 0.5, 0.75, 0.75, 0.5, 1, 0, 1]],
    ];
    const mid_tiles = [tiles[34], tiles[26], tiles[30], tiles[1], tiles[25], tiles[8], tiles[4]];

    // matrix/vector related
    function transformPoint(xy, mat) {
        var x1 = mat[0][0] * xy[0] + mat[0][1] * xy[1] + mat[0][2];
        var y1 = mat[1][0] * xy[0] + mat[1][1] * xy[1] + mat[1][2];
        return [x1, y1];
    }
    function matmul(a, b) {
        return [
            [
                a[0][0] * b[0][0] + a[0][1] * b[1][0],
                a[0][0] * b[0][1] + a[0][1] * b[1][1],
                a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2]
            ],
            [
                a[1][0] * b[0][0] + a[1][1] * b[1][0],
                a[1][0] * b[0][1] + a[1][1] * b[1][1],
                a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2]
            ]
        ];
    }

    // generate tiles (37 bits)
    function randomTransform(tile) {
        // 3 bit
        var sx = bitBuffer.nextBit() ? -1.0 : 1.0;
        var sy = bitBuffer.nextBit() ? -1.0 : 1.0;
        var mat = bitBuffer.nextBit() ?
            [[0, sx, 0], [sy, 0, 0]] : [[sx, 0, 0], [0, sy, 0]];
        mat = matmul([[1, 0, 0.5], [0, 1, 0.5]], matmul(mat, [[1, 0, -0.5], [0, 1, -0.5]]));
        var res = [];
        for (var si = 0; si < tile.length; si++) {
            var shape = [];
            for (var i = 0; i < tile[si].length; i += 2) {
                var p = transformPoint([tile[si][i], tile[si][i + 1]], mat);
                shape.push(p[0]), shape.push(p[1]);
            }
            res.push(shape.slice(0));
        }
        return res;
    }
    this.tile_00 = randomTransform(tiles[bitBuffer.nextInt(10) % tiles.length]);
    this.tile_10 = randomTransform(tiles[bitBuffer.nextInt(10) % tiles.length]);
    this.tile_11 = randomTransform(mid_tiles[bitBuffer.nextInt(8) % mid_tiles.length]);

    // color (25 bits)
    var r = bitBuffer.nextInt(8), g = bitBuffer.nextInt(8), b = bitBuffer.nextInt(8);
    var col = "rgb(" + [r, g, b].join(',') + ")";
    if (bitBuffer.nextBit())
        this.tilecol = col, this.backcol = "white";
    else
        this.tilecol = "white", this.backcol = col;

    // drawing
    this.renderCanvas = function (canvas, x, y, w, h) {
        const ctx = canvas.getContext("2d");

        function drawTile(tile, mat, backcol, tilecol) {
            var p0 = transformPoint([0, 0], mat);
            var p1 = transformPoint([1, 1], mat);
            ctx.fillStyle = backcol;
            ctx.fillRect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1]);
            ctx.fillStyle = tilecol;
            for (var si = 0; si < tile.length; si++) {
                var shape = tile[si];
                ctx.beginPath();
                for (var i = 0; i < shape.length; i += 2) {
                    var p = transformPoint([shape[i], shape[i + 1]], mat);
                    if (i == 0) ctx.moveTo(p[0], p[1]);
                    else ctx.lineTo(p[0], p[1]);
                }
                ctx.closePath();
                ctx.fill();
            }
        }

        for (var ai = 0; ai < 4; ai++) {
            var a = Math.PI * 0.5 * ai;
            var rotmat = [[Math.cos(a), -Math.sin(a), 0], [Math.sin(a), Math.cos(a), 0]];
            var trlmat = [[0.25 * w, 0, x + 0.5 * w], [0, 0.25 * h, y + 0.5 * h]];
            var mat = matmul(trlmat, rotmat);
            drawTile(this.tile_00,
                matmul(mat, [[1, 0, -2], [0, 1, -2]]),
                this.backcol, this.tilecol);
            drawTile(this.tile_10,
                matmul(mat, [[1, 0, -1], [0, 1, -2]]),
                this.backcol, this.tilecol);
            drawTile(this.tile_10,
                matmul(mat, [[1, 0, -2], [0, 1, -1]]),
                this.backcol, this.tilecol);
            drawTile(this.tile_11,
                matmul(mat, [[1, 0, -1], [0, 1, -1]]),
                this.backcol, this.tilecol);
        }
    };
}

