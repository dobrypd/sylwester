to_px = function (x) { return ''.concat(Math.round(x), 'px'); }
g_resize = function() { pgal.resize(); }
 
var pgal = { 
    O : [], N : 0, S : 0, img : 0, span : 0, xm : 0, ym : 0, nx : 0, ny : 0, nw : 0, nh : 0, 
    cx : 0, cy : 0, zoom : 1, x : 0, y : 0, z : -30000, xt : 0, yt : 0, zt : 0, 

    init : function () { 
        this.cx   = this.nw / 2; 
        this.cy   = this.nh / 2; 
        this.img  = document.getElementById('gall').getElementsByTagName('img'); 
        this.span  = document.getElementById('gall').getElementsByTagName('span'); 
        this.N    = this.img.length; 
        for (var i = 0; i < this.N; i++) this.O[i] = new this.PGObj(i); 
        this.run(); 
        this.O[0].click(); 
    }, 
    resize : function () { 
        var o   = document.getElementById('gall');
        this.nx   = o.offsetLeft; 
        this.ny   = o.offsetTop; 
        this.nw   = o.offsetWidth; 
        this.nh   = o.offsetHeight; 
        this.zoom = this.nh / 900; 
    }, 
    run : function () { 
        pgal.cx += (pgal.xm - pgal.cx) * .1; 
        pgal.cy += (pgal.ym - pgal.cy) * .1; 
        pgal.x  += (pgal.xt - pgal.x)  * .05; 
        pgal.y  += (pgal.yt - pgal.y)  * .05; 
        pgal.z  += (pgal.zt - pgal.z)  * .1; 
        var i = pgal.N; 
        while (i--) pgal.O[i].anim(); 
        setTimeout(pgal.run, 16); 
    },
    PGObj : function (n) {
        this.n                = n; 
        this.x                = pgal.zoom * Math.random() * pgal.nw * 3 - pgal.nw; 
        this.y                = pgal.zoom * Math.random() * pgal.nh * 3 - pgal.nh; 
        this.z                = Math.round(n * (10000 / pgal.N)); 
        this.w                = pgal.img[n].width; 
        this.h                = pgal.img[n].height; 
        this.oxt              = pgal.span[n]; 
        this.oxs              = this.oxt.style; 
        this.txt              = pgal.span[n].innerHTML; 
        this.oxt.innerHTML    = ""; 
        this.obj              = pgal.img[n]; 
        this.obs              = this.obj.style; 
        this.obj.parent       = this; 
        this.obj.onclick      = function() { this.parent.click(); } 
        this.obj.ondrag       = function() { return false; } 
        this.oxt.style.zIndex = this.obj.style.zIndex = Math.round(1000000 - this.z); 
        this.F                = false; 
        this.CF               = 100; 
        this.sto              = []; 

        this.anim = function() { 
            var f = 700 + this.z - pgal.z; 
            if (f > 0) { 
                var d               = 1000 / f; 
                var X               = pgal.nw * .5 + ((this.x - pgal.x - pgal.cx) * d); 
                var Y               = pgal.nh * .5 + ((this.y - pgal.y - pgal.cy) * d); 
                var W               = d * this.w * pgal.zoom; 
                var H               = d * this.h * pgal.zoom; 
                this.obs.left       = to_px(X - W * .5); 
                this.obs.top        = to_px(Y - H * .5); 
                this.obs.width      = to_px(W); 
                this.obs.height     = to_px(H); 
                this.oxs.visibility = (this.CF-- > 0 && Math.random() > .9) ? "hidden" : "visible"; 
                this.oxs.left       = to_px(X - W * .5); 
                this.oxs.top        = to_px(Y + H * .5); 
                if ((pgal.zt - pgal.z) < 20) { 
                    if (! this.F) { 
                        this.F            = true; 
                        this.CF           = Math.random() * 200; 
                        this.oxs.fontSize = to_px(1 + d * 20 * pgal.zoom); 
                        var T             = ""; 
                        var tn            = this.txt.length; 
                        for(var i = 0; i < tn; i++) { 
                            T = T.concat(this.txt.charAt(i)); 
                            this.sto[i] = setTimeout('pgal.O['.concat(n, '].oxt.innerHTML = "', T, '";'), Math.round(f / 4) + 10 * i);
                        } 
                    } 
                } else { 
                    this.F = false; 
                    this.oxt.innerHTML = ""; 
                } 
            } else { 
                this.x  = pgal.zoom * Math.random() * pgal.nw * 3 - pgal.nw; 
                this.y  = pgal.zoom * Math.random() * pgal.nh * 3 - pgal.nh; 
                this.z += 10000; 
                this.oxs.zIndex = this.obs.zIndex = Math.round(1000000 - this.z); 
            } 
        } 

        this.cto = function() { 
            var i = this.txt.length; 
            while (i--) clearTimeout(this.sto[i]); 
        } 

        this.click = function() { 
            var i = pgal.N; 
            while (i--) pgal.O[i].cto(); 
            if (pgal.S != this) { 
                pgal.xt = this.x; 
                pgal.yt = this.y; 
                pgal.zt = this.z; 
                pgal.S  = this; 
            } else { 
                pgal.S   = 0; 
                pgal.zt += 1600; 
            } 
        } 
    }
} 

// event handlers
window.onresize = g_resize;

document.onmousemove = function(e) { 
    if (window.event) e=window.event; 
    pgal.xm = (e.x || e.clientX) - pgal.nx - pgal.nw * .5; 
    pgal.ym = (e.y || e.clientY) - pgal.ny - pgal.nh * .5; 
}

var last = 0;
window.setInterval(function(){
	last++;
	last = last % 12;
    pgal.O[last].click();
}, 1000);

window.onload = function() { 
    g_resize(); 
    pgal.init(); 
}