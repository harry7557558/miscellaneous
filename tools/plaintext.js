// utf-8 encoding

/*
 * 
 */

"use strict";

function formatPlainText(src) {
    // split to array
    src = src.replace(/\n+$/g, '') + '\n';
    var arr = [], st = '';
    for (var i = 0; i < src.length; i++) {
        var c = src[i];
        if (c.match(/[A-Za-z]/)) {
            if (st != '' && !st.match(/[A-Za-z]$/)) arr.push(st), st = '';
            st += c;
        }
        else if (c.match(/[0-9]/)) {
            if (st != '' && !st.match(/[0-9]$/)) arr.push(st), st = '';
            st += c;
        }
        else {
            if (st != '') arr.push(st), st = '';
            arr.push(c);
        }
    }
    console.log(arr);

    // replace latex symbols
    {
        // https://katex.org/docs/supported.html
        // agressively "crawled", some are duplicated or not formatted
        const latex_list = [
            ['deg', '°'], ['sqrt', '√'], ['cbrt', '∛'], ['phi', 'φ'], ['stdphi', 'ϕ'],  // overriding latex standard
            ['Alpha', 'A'], ['Beta', 'B'], ['Gamma', 'Γ'], ['Delta', 'Δ'], ['Epsilon', 'E'], ['Zeta', 'Z'], ['Eta', 'H'], ['Theta', 'Θ'], ['Iota', 'I'], ['Kappa', 'K'], ['Lambda', 'Λ'], ['Mu', 'M'], ['Nu', 'N'], ['Xi', 'Ξ'], ['Omicron', 'O'], ['Pi', 'Π'], ['Rho', 'P'], ['Sigma', 'Σ'], ['Tau', 'T'], ['Upsilon', 'Υ'], ['Phi', 'Φ'], ['Chi', 'X'], ['Psi', 'Ψ'], ['Omega', 'Ω'], ['varGamma', 'Γ'], ['varDelta', 'Δ'], ['varTheta', 'Θ'], ['varLambda', 'Λ'], ['varXi', 'Ξ'], ['varPi', 'Π'], ['varSigma', 'Σ'], ['varUpsilon', 'Υ'], ['varPhi', 'Φ'], ['varPsi', 'Ψ'], ['varOmega', 'Ω'], ['alpha', 'α'], ['beta', 'β'], ['gamma', 'γ'], ['delta', 'δ'], ['epsilon', 'ϵ'], ['zeta', 'ζ'], ['eta', 'η'], ['theta', 'θ'], ['iota', 'ι'], ['kappa', 'κ'], ['lambda', 'λ'], ['mu', 'μ'], ['nu', 'ν'], ['xi', 'ξ'], ['omicron', 'ο'], ['pi', 'π'], ['rho', 'ρ'], ['sigma', 'σ'], ['tau', 'τ'], ['upsilon', 'υ'], ['phi', 'ϕ'], ['chi', 'χ'], ['psi', 'ψ'], ['omega', 'ω'], ['varepsilon', 'ε'], ['varkappa', 'ϰ'], ['vartheta', 'ϑ'], ['thetasym', 'ϑ'], ['varpi', 'ϖ'], ['varrho', 'ϱ'], ['varsigma', 'ς'], ['varphi', 'φ'], ['digamma', 'ϝ'],
            ['imath', ''], ['nabla', '∇'], ['Im', 'ℑ'], ['Reals', 'R'], ['jmath', ''], ['partial', '∂'], ['image', 'ℑ'], ['wp', '℘'], ['aleph', 'ℵ'], ['Game', '⅁'], ['Bbbk', 'k'], ['weierp', '℘'], ['alef', 'ℵ'], ['Finv', 'Ⅎ'], ['N', 'N'], ['Z', 'Z'], ['alefsym', 'ℵ'], ['cnums', 'C'], ['natnums', 'N'], ['beth', 'ℶ'], ['Complex', 'C'], ['R', 'R'], ['gimel', 'ℷ'], ['ell', 'ℓ'], ['Re', 'ℜ'], ['daleth', 'ℸ'], ['hbar', 'ℏ'], ['real', 'ℜ'], ['eth', 'ð'], ['hslash', 'ℏ'], ['reals', 'R'],
            ['forall', '∀'], ['complement', '∁'], ['therefore', '∴'], ['emptyset', '∅'], ['exists', '∃'], ['subset', '⊂'], ['because', '∵'], ['empty', '∅'], ['exist', '∃'], ['supset', '⊃'], ['mapsto', '↦'], ['varnothing', '∅'], ['nexists', '∄'], ['mid', '∣'], ['to', '→'], ['implies', '⟹'], ['in', '∈'], ['land', '∧'], ['gets', '←'], ['impliedby', '⟸'], ['isin', '∈'], ['lor', '∨'], ['leftrightarrow', '↔'], ['iff', '⟺'], ['notin', '∉'], ['ni', '∋'], ['notni', '∌'], ['neg', '¬'], ['lnot', '¬'],
            ['sum', '∑'], ['prod', '∏'], ['bigotimes', '⨂'], ['bigvee', '⋁'], ['int', '∫'], ['coprod', '∐'], ['bigoplus', '⨁'], ['bigwedge', '⋀'], ['iint', '∬'], ['intop', '∫'], ['bigodot', '⨀'], ['bigcap', '⋂'], ['iiint', '∭'], ['smallint', '∫'], ['biguplus', '⨄'], ['bigcup', '⋃'], ['oint', '∮'], ['oiint', '∯'], ['oiiint', '∰'], ['bigsqcup', '⨆'],
            ['cdot', '⋅'], ['gtrdot', '⋗'], ['cdotp', '⋅'], ['intercal', '⊺'], ['centerdot', '⋅'], ['land', '∧'], ['rhd', '⊳'], ['circ', '∘'], ['leftthreetimes', '⋋'], ['rightthreetimes', '⋌'], ['amalg', '⨿'], ['circledast', '⊛'], ['ldotp', '.'], ['rtimes', '⋊'], ['And', '&'], ['circledcirc', '⊚'], ['lor', '∨'], ['setminus', '∖'], ['ast', '∗'], ['circleddash', '⊝'], ['lessdot', '⋖'], ['smallsetminus', '∖'], ['barwedge', '⊼'], ['Cup', '⋓'], ['lhd', '⊲'], ['sqcap', '⊓'], ['bigcirc', '◯'], ['cup', '∪'], ['ltimes', '⋉'], ['sqcup', '⊔'], ['bmod', 'mod'], ['curlyvee', '⋎'], ['mod', 'x'], ['xmod', 'xmoda'], ['times', '×'], ['boxdot', '⊡'], ['curlywedge', '⋏'], ['mp', '∓'], ['unlhd', '⊴'], ['boxminus', '⊟'], ['div', '÷'], ['odot', '⊙'], ['unrhd', '⊵'], ['boxplus', '⊞'], ['divideontimes', '⋇'], ['ominus', '⊖'], ['uplus', '⊎'], ['boxtimes', '⊠'], ['dotplus', '∔'], ['oplus', '⊕'], ['vee', '∨'], ['bullet', '∙'], ['doublebarwedge', '⩞'], ['otimes', '⊗'], ['veebar', '⊻'], ['Cap', '⋒'], ['doublecap', '⋒'], ['oslash', '⊘'], ['wedge', '∧'], ['cap', '∩'], ['doublecup', '⋓'], ['pm', '±'], ['wr', '≀'],
            ['eqcirc', '≖'], ['lesseqgtr', '⋚'], ['sqsupset', '⊐'], ['eqcolon', '−:'], ['lesseqqgtr', '⪋'], ['sqsupseteq', '⊒'], ['Eqcolon', '−::'], ['lessgtr', '≶'], ['Subset', '⋐'], ['eqqcolon', '=:'], ['lesssim', '≲'], ['subset', '⊂'], ['sub', '⊂'], ['approx', '≈'], ['Eqqcolon', '=::'], ['ll', '≪'], ['approxeq', '≊'], ['eqsim', '≂'], ['lll', '⋘'], ['subseteqq', '⫅'], ['asymp', '≍'], ['eqslantgtr', '⪖'], ['llless', '⋘'], ['succ', '≻'], ['backepsilon', '∍'], ['eqslantless', '⪕'], ['lt', '<'], ['succapprox', '⪸'], ['backsim', '∽'], ['equiv', '≡'], ['mid', '∣'], ['succcurlyeq', '≽'], ['backsimeq', '⋍'], ['fallingdotseq', '≒'], ['models', '⊨'], ['succeq', '⪰'], ['between', '≬'], ['frown', '⌢'], ['multimap', '⊸'], ['succsim', '≿'], ['bowtie', '⋈'], ['ge', '≥'], ['owns', '∋'], ['Supset', '⋑'], ['bumpeq', '≏'], ['geq', '≥'], ['parallel', '∥'], ['supset', '⊃'], ['Bumpeq', '≎'], ['geqq', '≧'], ['perp', '⊥'], ['supseteq', '⊇'], ['supe', '⊇'], ['circeq', '≗'], ['geqslant', '⩾'], ['pitchfork', '⋔'], ['supseteqq', '⫆'], ['colonapprox', ':≈'], ['gg', '≫'], ['prec', '≺'], ['thickapprox', '≈'], ['Colonapprox', '::≈'], ['ggg', '⋙'], ['precapprox', '⪷'], ['thicksim', '∼'], ['coloneq', ':−'], ['gggtr', '⋙'], ['preccurlyeq', '≼'], ['trianglelefteq', '⊴'], ['Coloneq', '::−'], ['gt', '>'], ['preceq', '⪯'], ['triangleq', '≜'], ['coloneqq', ':='], ['gtrapprox', '⪆'], ['precsim', '≾'], ['trianglerighteq', '⊵'], ['Coloneqq', '::='], ['gtreqless', '⋛'], ['propto', '∝'], ['varpropto', '∝'], ['colonsim', ':∼'], ['gtreqqless', '⪌'], ['risingdotseq', '≓'], ['vartriangle', '△'], ['Colonsim', '::∼'], ['gtrless', '≷'], ['shortmid', '∣'], ['vartriangleleft', '⊲'], ['cong', '≅'], ['gtrsim', '≳'], ['shortparallel', '∥'], ['vartriangleright', '⊳'], ['curlyeqprec', '⋞'], ['in', '∈'], ['isin', '∈'], ['sim', '∼'], ['vcentcolon', ':'], ['curlyeqsucc', '⋟'], ['Join', '⋈'], ['simeq', '≃'], ['vdash', '⊢'], ['dashv', '⊣'], ['le', '≤'], ['smallfrown', '⌢'], ['vDash', '⊨'], ['dblcolon', '::'], ['leq', '≤'], ['smallsmile', '⌣'], ['Vdash', '⊩'], ['doteq', '≐'], ['leqq', '≦'], ['smile', '⌣'], ['Vvdash', '⊪'], ['Doteq', '≑'], ['leqslant', '⩽'], ['sqsubset', '⊏'], ['doteqdot', '≑'], ['lessapprox', '⪅'], ['sqsubseteq', '⊑'],
            ['circlearrowleft', '↺'], ['leftharpoonup', '↼'], ['rArr', '⇒'], ['circlearrowright', '↻'], ['leftleftarrows', '⇇'], ['rarr', '→'], ['curvearrowleft', '↶'], ['leftrightarrow', '↔'], ['restriction', '↾'], ['curvearrowright', '↷'], ['Leftrightarrow', '⇔'], ['rightarrow', '→'], ['Darr', '⇓'], ['leftrightarrows', '⇆'], ['Rightarrow', '⇒'], ['dArr', '⇓'], ['leftrightharpoons', '⇋'], ['rightarrowtail', '↣'], ['darr', '↓'], ['leftrightsquigarrow', '↭'], ['rightharpoondown', '⇁'], ['dashleftarrow', '⇠'], ['Lleftarrow', '⇚'], ['rightharpoonup', '⇀'], ['dashrightarrow', '⇢'], ['longleftarrow', '⟵'], ['rightleftarrows', '⇄'], ['downarrow', '↓'], ['Longleftarrow', '⟸'], ['rightleftharpoons', '⇌'], ['Downarrow', '⇓'], ['longleftrightarrow', '⟷'], ['rightrightarrows', '⇉'], ['downdownarrows', '⇊'], ['Longleftrightarrow', '⟺'], ['rightsquigarrow', '⇝'], ['downharpoonleft', '⇃'], ['longmapsto', '⟼'], ['Rrightarrow', '⇛'], ['downharpoonright', '⇂'], ['longrightarrow', '⟶'], ['Rsh', '↱'], ['gets', '←'], ['Longrightarrow', '⟹'], ['searrow', '↘'], ['Harr', '⇔'], ['looparrowleft', '↫'], ['swarrow', '↙'], ['hArr', '⇔'], ['looparrowright', '↬'], ['to', '→'], ['harr', '↔'], ['Lrarr', '⇔'], ['twoheadleftarrow', '↞'], ['hookleftarrow', '↩'], ['lrArr', '⇔'], ['twoheadrightarrow', '↠'], ['hookrightarrow', '↪'], ['lrarr', '↔'], ['Uarr', '⇑'], ['iff', '⟺'], ['Lsh', '↰'], ['uArr', '⇑'], ['impliedby', '⟸'], ['mapsto', '↦'], ['uarr', '↑'], ['implies', '⟹'], ['nearrow', '↗'], ['uparrow', '↑'], ['Larr', '⇐'], ['nleftarrow', '↚'], ['Uparrow', '⇑'], ['lArr', '⇐'], ['nLeftarrow', '⇍'], ['updownarrow', '↕'], ['larr', '←'], ['nleftrightarrow', '↮'], ['Updownarrow', '⇕'], ['leadsto', '⇝'], ['nLeftrightarrow', '⇎'], ['upharpoonleft', '↿'], ['leftarrow', '←'], ['nrightarrow', '↛'], ['upharpoonright', '↾'], ['Leftarrow', '⇐'], ['nRightarrow', '⇏'], ['upuparrows', '⇈'], ['leftarrowtail', '↢'], ['nwarrow', '↖'], ['leftharpoondown', '↽'], ['Rarr', '⇒'],
            ['dots', '…'], ['%', '%'], ['cdots', '⋯'], ['#', '#'], ['ddots', '⋱'], ['&', '&'], ['ldots', '…'], ['nabla', '∇'], ['_', '_'], ['vdots', '⋮'], ['infty', '∞'], ['dotsb', '⋯'], ['infin', '∞'], ['text{--}', '–'], ['dotsc', '…'], ['checkmark', '✓'], ['dotsi', '⋯'], ['dag', '†'], ['text{---}', '—'], ['dotsm', '⋯'], ['dagger', '†'], ['dotso', '…'], ['sdot', '⋅'], ['ddag', '‡'], ['mathellipsis', '…'], ['ddagger', '‡'], ['text{textquoteleft}', '‘'], ['Box', '□'], ['Dagger', '‡'], ['lq', '‘'], ['square', '□'], ['angle', '∠'], ['blacksquare', '■'], ['measuredangle', '∡'], ['triangle', '△'], ['sphericalangle', '∢'], ['triangledown', '▽'], ['top', '⊤'], ['triangleleft', '◃'], ['bot', '⊥'], ['triangleright', '▹'], ['$', '$'], ['colon', ':'], ['bigtriangledown', '▽'], ['backprime', '‵'], ['bigtriangleup', '△'], ['pounds', '£'], ['prime', '′'], ['blacktriangle', '▲'], ['mathsterling', '£'], ['blacktriangledown', '▼'], ['blacktriangleleft', '◀'], ['yen', '¥'], ['blacktriangleright', '▶'], ['surd', '√'], ['diamond', '⋄'], ['degree', '°'], ['Diamond', '◊'], ['lozenge', '◊'], ['mho', '℧'], ['blacklozenge', '⧫'], ['diagdown', '╲'], ['star', '⋆'], ['diagup', '╱'], ['bigstar', '★'], ['flat', '♭'], ['clubsuit', '♣'], ['natural', '♮'], ['clubs', '♣'], ['sharp', '♯'], ['circledR', '®'], ['diamondsuit', '♢'], ['heartsuit', '♡'], ['diamonds', '♢'], ['hearts', '♡'], ['circledS', 'Ⓢ'], ['spadesuit', '♠'], ['spades', '♠'], ['maltese', '✠'], ['minuso', '−'],
        ];
        for (var i = 1; i < arr.length; i++) {
            if (arr[i - 1] == '\\') {
                var idx = latex_list.map(x => x[0]).indexOf(arr[i]);
                if (idx != -1) {
                    arr[i - 1] = '';
                    arr[i] = latex_list[idx][1];
                }
                if (arr[i][0].match('[0-9A-Za-z]')) {
                    arr[i - 1] = '';
                }
            }
        }
        arr = arr.filter(function (e) { return e != ''; });
        console.log(arr);

        // brief handling of superscript/subscript
        const symbols = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-=(/)βγδθιΨχ";
        const supscpt = "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖqʳˢᵗᵘᵛʷˣʸᶻᴬᴮCᴰᴱFᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿSᵀᵁⱽᵂXYZ⁺⁻⁼⁽ᐟ⁾ᵝᵞᵟᶿᶥᵠᵡ";
        const subscpt = "₀₁₂₃₄₅₆₇₈₉ₐbcdₑfgₕᵢⱼₖₗₘₙₒₚqᵣₛₜᵤᵥwₓyzABCDEFGHIJKLMNOPQRSTUVWXYZ₊₋₌₍/₎ᵦᵧᵨθιᵩᵪ";
        for (var i = 0; i < arr.length - 1; i++) {
            if (arr[i] == '^') {
                var s = (arr[i + 1].split('')).map(c => (function (c) {
                    var d = symbols.indexOf(c);
                    return d == -1 ? c : supscpt[d];
                })(c)).join('');
                if (s != arr[i + 1]) arr[i] = '';
                arr[i + 1] = s;
            }
            if (arr[i] == '_') {
                var s = (arr[i + 1].split('')).map(c => (function (c) {
                    var d = symbols.indexOf(c);
                    return d == -1 ? c : subscpt[d];
                })(c)).join('');
                if (s != arr[i + 1]) arr[i] = '';
                arr[i + 1] = s;
            }
        }
    }

    return arr.join('').replace(/\n$/, '');
};


(window.onclick = function () {
    var s = document.getElementsByTagName('textarea')[0];
    if (s != undefined) {
        s.onkeydown = function (e) {
            if (e.keyCode == 9) {
                e.preventDefault();
                var msg = formatPlainText(s.value);
                s.value = msg;
                s.setAttribute('data-initial-value', msg);
            }
        }
    }
}
)();
