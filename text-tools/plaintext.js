// utf-8 encoding

// Used to quickly type LaTeX-style symbols in plain text

// Deprecated -
// Use for typing equations in Google meet messages
// Enter plain-text equation in the chatbox, press Tab, the equation will be formatted using Unicode characters

"use strict";


// Discord emojis as in March 2022, without diversity
const EMOJIS = (function (emojis) {
    emojis = emojis.split(';');
    console.log(emojis.length);
    var dict = {};
    for (var i = 0; i < emojis.length; i++) {
        var emoji = emojis[i].split(',');
        dict[emoji[0]] = emoji[1];
    }
    return dict;
})(
    "+1,👍;-1,👎;100,💯;1234,🔢;8ball,🎱;a,🅰️;ab,🆎;abacus,🧮;abc,🔤;abcd,🔡;accept,🉑;accordion,🪗;adhesive_bandage,🩹;admission_tickets,🎟️;adult,🧑;aerial_tramway,🚡;airplane,✈️;airplane_arriving,🛬;airplane_departure,🛫;airplane_small,🛩️;alarm_clock,⏰;alembic,⚗️;alien,👽;ambulance,🚑;amphora,🏺;anatomical_heart,🫀;anchor,⚓;angel,👼;anger,💢;anger_right,🗯️;angry,😠;anguished,😧;ant,🐜;apple,🍎;aquarius,♒;archery,🏹;aries,♈;arrow_backward,◀️;arrow_double_down,⏬;arrow_double_up,⏫;arrow_down,⬇️;arrow_down_small,🔽;arrow_forward,▶️;arrow_heading_down,⤵️;arrow_heading_up,⤴️;arrow_left,⬅️;arrow_lower_left,↙️;arrow_lower_right,↘️;arrow_right,➡️;arrow_right_hook,↪️;arrow_up,⬆️;arrow_up_down,↕️;arrow_up_small,🔼;arrow_upper_left,↖️;arrow_upper_right,↗️;arrows_clockwise,🔃;arrows_counterclockwise,🔄;art,🎨;articulated_lorry,🚛;artist,🧑‍🎨;asterisk,*️⃣;astonished,😲;astronaut,🧑‍🚀;athletic_shoe,👟;atm,🏧;atom,⚛️;atom_symbol,⚛️;auto_rickshaw,🛺;avocado,🥑;axe,🪓;b,🅱️;baby,👶;baby_bottle,🍼;baby_chick,🐤;baby_symbol,🚼;back,🔙;back_of_hand,🤚;bacon,🥓;badger,🦡;badminton,🏸;bagel,🥯;baggage_claim,🛄;baguette_bread,🥖;ballet_shoes,🩰;balloon,🎈;ballot_box,🗳️;ballot_box_with_ballot,🗳️;ballot_box_with_check,☑️;bamboo,🎍;banana,🍌;bangbang,‼️;banjo,🪕;bank,🏦;bar_chart,📊;barber,💈;baseball,⚾;basket,🧺;basketball,🏀;basketball_player,⛹️;bat,🦇;bath,🛀;bathtub,🛁;battery,🔋;beach,🏖️;beach_umbrella,⛱️;beach_with_umbrella,🏖️;beans,🫘;bear,🐻;bearded_person,🧔;beaver,🦫;bed,🛏️;bee,🐝;beer,🍺;beers,🍻;beetle,🪲;beginner,🔰;bell,🔔;bell_pepper,🫑;bellhop,🛎️;bellhop_bell,🛎️;bento,🍱;beverage_box,🧃;bicyclist,🚴;bike,🚲;bikini,👙;billed_cap,🧢;biohazard,☣️;biohazard_sign,☣️;bird,🐦;birthday,🎂;bison,🦬;biting_lip,🫦;black_cat,🐈‍⬛;black_circle,⚫;black_heart,🖤;black_joker,🃏;black_large_square,⬛;black_medium_small_square,◾;black_medium_square,◼️;black_nib,✒️;black_small_square,▪️;black_square_button,🔲;blond_haired_man,👱‍♂️;blond_haired_person,👱;blond_haired_woman,👱‍♀️;blossom,🌼;blowfish,🐡;blue_book,📘;blue_car,🚙;blue_circle,🔵;blue_heart,💙;blue_square,🟦;blueberries,🫐;blush,😊;boar,🐗;bomb,💣;bone,🦴;book,📖;bookmark,🔖;bookmark_tabs,📑;books,📚;boom,💥;boomerang,🪃;boot,👢;bottle_with_popping_cork,🍾;bouquet,💐;bow,🙇;bow_and_arrow,🏹;bowl_with_spoon,🥣;bowling,🎳;boxing_glove,🥊;boxing_gloves,🥊;boy,👦;brain,🧠;bread,🍞;breast_feeding,🤱;bricks,🧱;bride_with_veil,👰‍♀️;bridge_at_night,🌉;briefcase,💼;briefs,🩲;broccoli,🥦;broken_heart,💔;broom,🧹;brown_circle,🟤;brown_heart,🤎;brown_square,🟫;bubble_tea,🧋;bubbles,🫧;bucket,🪣;bug,🐛;building_construction,🏗️;bulb,💡;bullettrain_front,🚅;bullettrain_side,🚄;burrito,🌯;bus,🚌;busstop,🚏;bust_in_silhouette,👤;busts_in_silhouette,👥;butter,🧈;butterfly,🦋;cactus,🌵;cake,🍰;calendar,📆;calendar_spiral,🗓️;call_me,🤙;call_me_hand,🤙;calling,📲;camel,🐫;camera,📷;camera_with_flash,📸;camping,🏕️;cancer,♋;candle,🕯️;candy,🍬;canned_food,🥫;canoe,🛶;capital_abcd,🔠;capricorn,♑;card_box,🗃️;card_file_box,🗃️;card_index,📇;card_index_dividers,🗂️;carousel_horse,🎠;carpentry_saw,🪚;carrot,🥕;cartwheel,🤸;cat,🐱;cat2,🐈;cd,💿;chains,⛓️;chair,🪑;champagne,🍾;champagne_glass,🥂;chart,💹;chart_with_downwards_trend,📉;chart_with_upwards_trend,📈;checkered_flag,🏁;cheese,🧀;cheese_wedge,🧀;cherries,🍒;cherry_blossom,🌸;chess_pawn,♟️;chestnut,🌰;chicken,🐔;child,🧒;children_crossing,🚸;chipmunk,🐿️;chocolate_bar,🍫;chopsticks,🥢;christmas_tree,🎄;church,⛪;cinema,🎦;circus_tent,🎪;city_dusk,🌆;city_sunrise,🌇;city_sunset,🌇;cityscape,🏙️;cl,🆑;clap,👏;clapper,🎬;classical_building,🏛️;clinking_glass,🥂;clipboard,📋;clock,🕰️;clock1,🕐;clock10,🕙;clock1030,🕥;clock11,🕚;clock1130,🕦;clock12,🕛;clock1230,🕧;clock130,🕜;clock2,🕑;clock230,🕝;clock3,🕒;clock330,🕞;clock4,🕓;clock430,🕟;clock5,🕔;clock530,🕠;clock6,🕕;clock630,🕡;clock7,🕖;clock730,🕢;clock8,🕗;clock830,🕣;clock9,🕘;clock930,🕤;closed_book,📕;closed_lock_with_key,🔐;closed_umbrella,🌂;cloud,☁️;cloud_lightning,🌩️;cloud_rain,🌧️;cloud_snow,🌨️;cloud_tornado,🌪️;cloud_with_lightning,🌩️;cloud_with_rain,🌧️;cloud_with_snow,🌨️;cloud_with_tornado,🌪️;clown,🤡;clown_face,🤡;clubs,♣️;coat,🧥;cockroach,🪳;cocktail,🍸;coconut,🥥;coffee,☕;coffin,⚰️;coin,🪙;cold_face,🥶;cold_sweat,😰;comet,☄️;compass,🧭;compression,🗜️;computer,💻;confetti_ball,🎊;confounded,😖;confused,😕;congratulations,㊗️;construction,🚧;construction_site,🏗️;construction_worker,👷;control_knobs,🎛️;convenience_store,🏪;cook,🧑‍🍳;cookie,🍪;cooking,🍳;cool,🆒;cop,👮;copyright,©️;coral,🪸;corn,🌽;couch,🛋️;couch_and_lamp,🛋️;couple,👫;couple_mm,👨‍❤️‍👨;couple_with_heart,💑;couple_with_heart_mm,👨‍❤️‍👨;couple_with_heart_woman_man,👩‍❤️‍👨;couple_with_heart_ww,👩‍❤️‍👩;couple_ww,👩‍❤️‍👩;couplekiss,💏;couplekiss_mm,👨‍❤️‍💋‍👨;couplekiss_ww,👩‍❤️‍💋‍👩;cow,🐮;cow2,🐄;cowboy,🤠;crab,🦀;crayon,🖍️;credit_card,💳;crescent_moon,🌙;cricket,🦗;cricket_bat_ball,🏏;cricket_game,🏏;crocodile,🐊;croissant,🥐;cross,✝️;crossed_flags,🎌;crossed_swords,⚔️;crown,👑;cruise_ship,🛳️;crutch,🩼;cry,😢;crying_cat_face,😿;crystal_ball,🔮;cucumber,🥒;cup_with_straw,🥤;cupcake,🧁;cupid,💘;curling_stone,🥌;curly_loop,➰;currency_exchange,💱;curry,🍛;custard,🍮;customs,🛃;cut_of_meat,🥩;cyclone,🌀;dagger,🗡️;dagger_knife,🗡️;dancer,💃;dancers,👯;dango,🍡;dark_sunglasses,🕶️;dart,🎯;dash,💨;date,📅;deaf_man,🧏‍♂️;deaf_person,🧏;deaf_woman,🧏‍♀️;deciduous_tree,🌳;deer,🦌;department_store,🏬;derelict_house_building,🏚️;desert,🏜️;desert_island,🏝️;desktop,🖥️;desktop_computer,🖥️;detective,🕵️;diamond_shape_with_a_dot_inside,💠;diamonds,♦️;disappointed,😞;disappointed_relieved,😥;disguised_face,🥸;dividers,🗂️;diving_mask,🤿;diya_lamp,🪔;dizzy,💫;dizzy_face,😵;dna,🧬;do_not_litter,🚯;dodo,🦤;dog,🐶;dog2,🐕;dollar,💵;dolls,🎎;dolphin,🐬;door,🚪;dotted_line_face,🫥;double_vertical_bar,⏸️;doughnut,🍩;dove,🕊️;dove_of_peace,🕊️;dragon,🐉;dragon_face,🐲;dress,👗;dromedary_camel,🐪;drool,🤤;drooling_face,🤤;drop_of_blood,🩸;droplet,💧;drum,🥁;drum_with_drumsticks,🥁;duck,🦆;dumpling,🥟;dvd,📀;e_mail,📧;eagle,🦅;ear,👂;ear_of_rice,🌾;ear_with_hearing_aid,🦻;earth_africa,🌍;earth_americas,🌎;earth_asia,🌏;egg,🥚;eggplant,🍆;eight,8️⃣;eight_pointed_black_star,✴️;eight_spoked_asterisk,✳️;eject,⏏️;eject_symbol,⏏️;electric_plug,🔌;elephant,🐘;elevator,🛗;elf,🧝;email,📧;empty_nest,🪹;end,🔚;england,🏴󠁧󠁢󠁥󠁮󠁧󠁿;envelope,✉️;envelope_with_arrow,📩;euro,💶;european_castle,🏰;european_post_office,🏤;evergreen_tree,🌲;exclamation,❗;expecting_woman,🤰;exploding_head,🤯;expressionless,😑;eye,👁️;eye_in_speech_bubble,👁‍🗨;eyeglasses,👓;eyes,👀;face_exhaling,😮‍💨;face_holding_back_tears,🥹;face_in_clouds,😶‍🌫️;face_palm,🤦;face_vomiting,🤮;face_with_cowboy_hat,🤠;face_with_diagonal_mouth,🫤;face_with_hand_over_mouth,🤭;face_with_head_bandage,🤕;face_with_monocle,🧐;face_with_open_eyes_and_hand_over_mouth,🫢;face_with_peeking_eye,🫣;face_with_raised_eyebrow,🤨;face_with_rolling_eyes,🙄;face_with_spiral_eyes,😵‍💫;face_with_symbols_over_mouth,🤬;face_with_thermometer,🤒;facepalm,🤦;factory,🏭;factory_worker,🧑‍🏭;fairy,🧚;falafel,🧆;fallen_leaf,🍂;family,👪;family_man_boy,👨‍👦;family_man_boy_boy,👨‍👦‍👦;family_man_girl,👨‍👧;family_man_girl_boy,👨‍👧‍👦;family_man_girl_girl,👨‍👧‍👧;family_man_woman_boy,👨‍👩‍👦;family_mmb,👨‍👨‍👦;family_mmbb,👨‍👨‍👦‍👦;family_mmg,👨‍👨‍👧;family_mmgb,👨‍👨‍👧‍👦;family_mmgg,👨‍👨‍👧‍👧;family_mwbb,👨‍👩‍👦‍👦;family_mwg,👨‍👩‍👧;family_mwgb,👨‍👩‍👧‍👦;family_mwgg,👨‍👩‍👧‍👧;family_woman_boy,👩‍👦;family_woman_boy_boy,👩‍👦‍👦;family_woman_girl,👩‍👧;family_woman_girl_boy,👩‍👧‍👦;family_woman_girl_girl,👩‍👧‍👧;family_wwb,👩‍👩‍👦;family_wwbb,👩‍👩‍👦‍👦;family_wwg,👩‍👩‍👧;family_wwgb,👩‍👩‍👧‍👦;family_wwgg,👩‍👩‍👧‍👧;farmer,🧑‍🌾;fast_forward,⏩;fax,📠;fearful,😨;feather,🪶;feet,🐾;female_sign,♀️;fencer,🤺;fencing,🤺;ferris_wheel,🎡;ferry,⛴️;field_hockey,🏑;file_cabinet,🗄️;file_folder,📁;film_frames,🎞️;film_projector,📽️;fingers_crossed,🤞;fire,🔥;fire_engine,🚒;fire_extinguisher,🧯;firecracker,🧨;firefighter,🧑‍🚒;fireworks,🎆;first_place,🥇;first_place_medal,🥇;first_quarter_moon,🌓;first_quarter_moon_with_face,🌛;fish,🐟;fish_cake,🍥;fishing_pole_and_fish,🎣;fist,✊;five,5️⃣;flag_ac,🇦🇨;flag_ad,🇦🇩;flag_ae,🇦🇪;flag_af,🇦🇫;flag_ag,🇦🇬;flag_ai,🇦🇮;flag_al,🇦🇱;flag_am,🇦🇲;flag_ao,🇦🇴;flag_aq,🇦🇶;flag_ar,🇦🇷;flag_as,🇦🇸;flag_at,🇦🇹;flag_au,🇦🇺;flag_aw,🇦🇼;flag_ax,🇦🇽;flag_az,🇦🇿;flag_ba,🇧🇦;flag_bb,🇧🇧;flag_bd,🇧🇩;flag_be,🇧🇪;flag_bf,🇧🇫;flag_bg,🇧🇬;flag_bh,🇧🇭;flag_bi,🇧🇮;flag_bj,🇧🇯;flag_bl,🇧🇱;flag_black,🏴;flag_bm,🇧🇲;flag_bn,🇧🇳;flag_bo,🇧🇴;flag_bq,🇧🇶;flag_br,🇧🇷;flag_bs,🇧🇸;flag_bt,🇧🇹;flag_bv,🇧🇻;flag_bw,🇧🇼;flag_by,🇧🇾;flag_bz,🇧🇿;flag_ca,🇨🇦;flag_cc,🇨🇨;flag_cd,🇨🇩;flag_cf,🇨🇫;flag_cg,🇨🇬;flag_ch,🇨🇭;flag_ci,🇨🇮;flag_ck,🇨🇰;flag_cl,🇨🇱;flag_cm,🇨🇲;flag_cn,🇨🇳;flag_co,🇨🇴;flag_cp,🇨🇵;flag_cr,🇨🇷;flag_cu,🇨🇺;flag_cv,🇨🇻;flag_cw,🇨🇼;flag_cx,🇨🇽;flag_cy,🇨🇾;flag_cz,🇨🇿;flag_de,🇩🇪;flag_dg,🇩🇬;flag_dj,🇩🇯;flag_dk,🇩🇰;flag_dm,🇩🇲;flag_do,🇩🇴;flag_dz,🇩🇿;flag_ea,🇪🇦;flag_ec,🇪🇨;flag_ee,🇪🇪;flag_eg,🇪🇬;flag_eh,🇪🇭;flag_er,🇪🇷;flag_es,🇪🇸;flag_et,🇪🇹;flag_eu,🇪🇺;flag_fi,🇫🇮;flag_fj,🇫🇯;flag_fk,🇫🇰;flag_fm,🇫🇲;flag_fo,🇫🇴;flag_fr,🇫🇷;flag_ga,🇬🇦;flag_gb,🇬🇧;flag_gd,🇬🇩;flag_ge,🇬🇪;flag_gf,🇬🇫;flag_gg,🇬🇬;flag_gh,🇬🇭;flag_gi,🇬🇮;flag_gl,🇬🇱;flag_gm,🇬🇲;flag_gn,🇬🇳;flag_gp,🇬🇵;flag_gq,🇬🇶;flag_gr,🇬🇷;flag_gs,🇬🇸;flag_gt,🇬🇹;flag_gu,🇬🇺;flag_gw,🇬🇼;flag_gy,🇬🇾;flag_hk,🇭🇰;flag_hm,🇭🇲;flag_hn,🇭🇳;flag_hr,🇭🇷;flag_ht,🇭🇹;flag_hu,🇭🇺;flag_ic,🇮🇨;flag_id,🇮🇩;flag_ie,🇮🇪;flag_il,🇮🇱;flag_im,🇮🇲;flag_in,🇮🇳;flag_io,🇮🇴;flag_iq,🇮🇶;flag_ir,🇮🇷;flag_is,🇮🇸;flag_it,🇮🇹;flag_je,🇯🇪;flag_jm,🇯🇲;flag_jo,🇯🇴;flag_jp,🇯🇵;flag_ke,🇰🇪;flag_kg,🇰🇬;flag_kh,🇰🇭;flag_ki,🇰🇮;flag_km,🇰🇲;flag_kn,🇰🇳;flag_kp,🇰🇵;flag_kr,🇰🇷;flag_kw,🇰🇼;flag_ky,🇰🇾;flag_kz,🇰🇿;flag_la,🇱🇦;flag_lb,🇱🇧;flag_lc,🇱🇨;flag_li,🇱🇮;flag_lk,🇱🇰;flag_lr,🇱🇷;flag_ls,🇱🇸;flag_lt,🇱🇹;flag_lu,🇱🇺;flag_lv,🇱🇻;flag_ly,🇱🇾;flag_ma,🇲🇦;flag_mc,🇲🇨;flag_md,🇲🇩;flag_me,🇲🇪;flag_mf,🇲🇫;flag_mg,🇲🇬;flag_mh,🇲🇭;flag_mk,🇲🇰;flag_ml,🇲🇱;flag_mm,🇲🇲;flag_mn,🇲🇳;flag_mo,🇲🇴;flag_mp,🇲🇵;flag_mq,🇲🇶;flag_mr,🇲🇷;flag_ms,🇲🇸;flag_mt,🇲🇹;flag_mu,🇲🇺;flag_mv,🇲🇻;flag_mw,🇲🇼;flag_mx,🇲🇽;flag_my,🇲🇾;flag_mz,🇲🇿;flag_na,🇳🇦;flag_nc,🇳🇨;flag_ne,🇳🇪;flag_nf,🇳🇫;flag_ng,🇳🇬;flag_ni,🇳🇮;flag_nl,🇳🇱;flag_no,🇳🇴;flag_np,🇳🇵;flag_nr,🇳🇷;flag_nu,🇳🇺;flag_nz,🇳🇿;flag_om,🇴🇲;flag_pa,🇵🇦;flag_pe,🇵🇪;flag_pf,🇵🇫;flag_pg,🇵🇬;flag_ph,🇵🇭;flag_pk,🇵🇰;flag_pl,🇵🇱;flag_pm,🇵🇲;flag_pn,🇵🇳;flag_pr,🇵🇷;flag_ps,🇵🇸;flag_pt,🇵🇹;flag_pw,🇵🇼;flag_py,🇵🇾;flag_qa,🇶🇦;flag_re,🇷🇪;flag_ro,🇷🇴;flag_rs,🇷🇸;flag_ru,🇷🇺;flag_rw,🇷🇼;flag_sa,🇸🇦;flag_sb,🇸🇧;flag_sc,🇸🇨;flag_sd,🇸🇩;flag_se,🇸🇪;flag_sg,🇸🇬;flag_sh,🇸🇭;flag_si,🇸🇮;flag_sj,🇸🇯;flag_sk,🇸🇰;flag_sl,🇸🇱;flag_sm,🇸🇲;flag_sn,🇸🇳;flag_so,🇸🇴;flag_sr,🇸🇷;flag_ss,🇸🇸;flag_st,🇸🇹;flag_sv,🇸🇻;flag_sx,🇸🇽;flag_sy,🇸🇾;flag_sz,🇸🇿;flag_ta,🇹🇦;flag_tc,🇹🇨;flag_td,🇹🇩;flag_tf,🇹🇫;flag_tg,🇹🇬;flag_th,🇹🇭;flag_tj,🇹🇯;flag_tk,🇹🇰;flag_tl,🇹🇱;flag_tm,🇹🇲;flag_tn,🇹🇳;flag_to,🇹🇴;flag_tr,🇹🇷;flag_tt,🇹🇹;flag_tv,🇹🇻;flag_tw,🇹🇼;flag_tz,🇹🇿;flag_ua,🇺🇦;flag_ug,🇺🇬;flag_um,🇺🇲;flag_us,🇺🇸;flag_uy,🇺🇾;flag_uz,🇺🇿;flag_va,🇻🇦;flag_vc,🇻🇨;flag_ve,🇻🇪;flag_vg,🇻🇬;flag_vi,🇻🇮;flag_vn,🇻🇳;flag_vu,🇻🇺;flag_wf,🇼🇫;flag_white,🏳️;flag_ws,🇼🇸;flag_xk,🇽🇰;flag_ye,🇾🇪;flag_yt,🇾🇹;flag_za,🇿🇦;flag_zm,🇿🇲;flag_zw,🇿🇼;flags,🎏;flame,🔥;flamingo,🦩;flan,🍮;flashlight,🔦;flatbread,🫓;fleur_de_lis,⚜️;floppy_disk,💾;flower_playing_cards,🎴;flushed,😳;fly,🪰;flying_disc,🥏;flying_saucer,🛸;fog,🌫️;foggy,🌁;fondue,🫕;foot,🦶;football,🏈;footprints,👣;fork_and_knife,🍴;fork_and_knife_with_plate,🍽️;fork_knife_plate,🍽️;fortune_cookie,🥠;fountain,⛲;four,4️⃣;four_leaf_clover,🍀;fox,🦊;fox_face,🦊;frame_photo,🖼️;frame_with_picture,🖼️;free,🆓;french_bread,🥖;fried_shrimp,🍤;fries,🍟;frog,🐸;frowning,😦;frowning2,☹️;fuelpump,⛽;full_moon,🌕;full_moon_with_face,🌝;funeral_urn,⚱️;game_die,🎲;garlic,🧄;gay_pride_flag,🏳️‍🌈;gear,⚙️;gem,💎;gemini,♊;genie,🧞;ghost,👻;gift,🎁;gift_heart,💝;giraffe,🦒;girl,👧;glass_of_milk,🥛;globe_with_meridians,🌐;gloves,🧤;goal,🥅;goal_net,🥅;goat,🐐;goggles,🥽;golf,⛳;golfer,🏌️;gorilla,🦍;grandma,👵;grapes,🍇;green_apple,🍏;green_book,📗;green_circle,🟢;green_heart,💚;green_salad,🥗;green_square,🟩;grey_exclamation,❕;grey_question,❔;grimacing,😬;grin,😁;grinning,😀;guard,💂;guardsman,💂;guide_dog,🦮;guitar,🎸;gun,🔫;haircut,💇;hamburger,🍔;hammer,🔨;hammer_and_pick,⚒️;hammer_and_wrench,🛠️;hammer_pick,⚒️;hamsa,🪬;hamster,🐹;hand_splayed,🖐️;hand_with_index_and_middle_finger_crossed,🤞;hand_with_index_finger_and_thumb_crossed,🫰;handbag,👜;handball,🤾;handshake,🤝;hankey,💩;hash,#️⃣;hatched_chick,🐥;hatching_chick,🐣;head_bandage,🤕;headphones,🎧;headstone,🪦;health_worker,🧑‍⚕️;hear_no_evil,🙉;heart,❤️;heart_decoration,💟;heart_exclamation,❣️;heart_eyes,😍;heart_eyes_cat,😻;heart_hands,🫶;heart_on_fire,❤️‍🔥;heartbeat,💓;heartpulse,💗;hearts,♥️;heavy_check_mark,✔️;heavy_division_sign,➗;heavy_dollar_sign,💲;heavy_equals_sign,🟰;heavy_heart_exclamation_mark_ornament,❣️;heavy_minus_sign,➖;heavy_multiplication_x,✖️;heavy_plus_sign,➕;hedgehog,🦔;helicopter,🚁;helmet_with_cross,⛑️;helmet_with_white_cross,⛑️;herb,🌿;hibiscus,🌺;high_brightness,🔆;high_heel,👠;hiking_boot,🥾;hindu_temple,🛕;hippopotamus,🦛;hockey,🏒;hole,🕳️;homes,🏘️;honey_pot,🍯;hook,🪝;horse,🐴;horse_racing,🏇;hospital,🏥;hot_dog,🌭;hot_face,🥵;hot_pepper,🌶️;hotdog,🌭;hotel,🏨;hotsprings,♨️;hourglass,⌛;hourglass_flowing_sand,⏳;house,🏠;house_abandoned,🏚️;house_buildings,🏘️;house_with_garden,🏡;hugging,🤗;hugging_face,🤗;hushed,😯;hut,🛖;ice_cream,🍨;ice_cube,🧊;ice_skate,⛸️;icecream,🍦;id,🆔;identification_card,🪪;ideograph_advantage,🉐;imp,👿;inbox_tray,📥;incoming_envelope,📨;index_pointing_at_the_viewer,🫵;infinity,♾️;information_desk_person,💁;information_source,ℹ️;innocent,😇;interrobang,⁉️;iphone,📱;island,🏝️;izakaya_lantern,🏮;jack_o_lantern,🎃;japan,🗾;japanese_castle,🏯;japanese_goblin,👺;japanese_ogre,👹;jar,🫙;jeans,👖;jigsaw,🧩;joy,😂;joy_cat,😹;joystick,🕹️;judge,🧑‍⚖️;juggler,🤹;juggling,🤹;kaaba,🕋;kangaroo,🦘;karate_uniform,🥋;kayak,🛶;key,🔑;key2,🗝️;keyboard,⌨️;keycap_asterisk,*️⃣;keycap_ten,🔟;kimono,👘;kiss,💋;kiss_mm,👨‍❤️‍💋‍👨;kiss_woman_man,👩‍❤️‍💋‍👨;kiss_ww,👩‍❤️‍💋‍👩;kissing,😗;kissing_cat,😽;kissing_closed_eyes,😚;kissing_heart,😘;kissing_smiling_eyes,😙;kite,🪁;kiwi,🥝;kiwifruit,🥝;knife,🔪;knot,🪢;koala,🐨;koko,🈁;lab_coat,🥼;label,🏷️;lacrosse,🥍;ladder,🪜;lady_beetle,🐞;large_blue_diamond,🔷;large_orange_diamond,🔶;last_quarter_moon,🌗;last_quarter_moon_with_face,🌜;latin_cross,✝️;laughing,😆;leafy_green,🥬;leaves,🍃;ledger,📒;left_facing_fist,🤛;left_fist,🤛;left_luggage,🛅;left_right_arrow,↔️;left_speech_bubble,🗨️;leftwards_arrow_with_hook,↩️;leftwards_hand,🫲;leg,🦵;lemon,🍋;leo,♌;leopard,🐆;level_slider,🎚️;levitate,🕴️;liar,🤥;libra,♎;lifter,🏋️;light_rail,🚈;link,🔗;linked_paperclips,🖇️;lion,🦁;lion_face,🦁;lips,👄;lipstick,💄;lizard,🦎;llama,🦙;lobster,🦞;lock,🔒;lock_with_ink_pen,🔏;lollipop,🍭;long_drum,🪘;loop,➿;lotus,🪷;loud_sound,🔊;loudspeaker,📢;love_hotel,🏩;love_letter,💌;love_you_gesture,🤟;low_battery,🪫;low_brightness,🔅;lower_left_ballpoint_pen,🖊️;lower_left_crayon,🖍️;lower_left_fountain_pen,🖋️;lower_left_paintbrush,🖌️;luggage,🧳;lungs,🫁;lying_face,🤥;m,Ⓜ️;mag,🔍;mag_right,🔎;mage,🧙;magic_wand,🪄;magnet,🧲;mahjong,🀄;mailbox,📫;mailbox_closed,📪;mailbox_with_mail,📬;mailbox_with_no_mail,📭;male_dancer,🕺;male_sign,♂️;mammoth,🦣;man,👨;man_artist,👨‍🎨;man_astronaut,👨‍🚀;man_bald,👨‍🦲;man_beard,🧔‍♂️;man_biking,🚴‍♂️;man_bouncing_ball,⛹️‍♂️;man_bowing,🙇‍♂️;man_cartwheeling,🤸‍♂️;man_climbing,🧗‍♂️;man_construction_worker,👷‍♂️;man_cook,👨‍🍳;man_curly_haired,👨‍🦱;man_dancing,🕺;man_detective,🕵️‍♂️;man_elf,🧝‍♂️;man_facepalming,🤦‍♂️;man_factory_worker,👨‍🏭;man_fairy,🧚‍♂️;man_farmer,👨‍🌾;man_feeding_baby,👨‍🍼;man_firefighter,👨‍🚒;man_frowning,🙍‍♂️;man_genie,🧞‍♂️;man_gesturing_no,🙅‍♂️;man_gesturing_ok,🙆‍♂️;man_getting_face_massage,💆‍♂️;man_getting_haircut,💇‍♂️;man_golfing,🏌️‍♂️;man_guard,💂‍♂️;man_health_worker,👨‍⚕️;man_in_business_suit_levitating,🕴️;man_in_lotus_position,🧘‍♂️;man_in_manual_wheelchair,👨‍🦽;man_in_motorized_wheelchair,👨‍🦼;man_in_steamy_room,🧖‍♂️;man_in_tuxedo,🤵‍♂️;man_judge,👨‍⚖️;man_juggling,🤹‍♂️;man_kneeling,🧎‍♂️;man_lifting_weights,🏋️‍♂️;man_mage,🧙‍♂️;man_mechanic,👨‍🔧;man_mountain_biking,🚵‍♂️;man_office_worker,👨‍💼;man_pilot,👨‍✈️;man_playing_handball,🤾‍♂️;man_playing_water_polo,🤽‍♂️;man_police_officer,👮‍♂️;man_pouting,🙎‍♂️;man_raising_hand,🙋‍♂️;man_red_haired,👨‍🦰;man_rowing_boat,🚣‍♂️;man_running,🏃‍♂️;man_scientist,👨‍🔬;man_shrugging,🤷‍♂️;man_singer,👨‍🎤;man_standing,🧍‍♂️;man_student,👨‍🎓;man_superhero,🦸‍♂️;man_supervillain,🦹‍♂️;man_surfing,🏄‍♂️;man_swimming,🏊‍♂️;man_teacher,👨‍🏫;man_technologist,👨‍💻;man_tipping_hand,💁‍♂️;man_vampire,🧛‍♂️;man_walking,🚶‍♂️;man_wearing_turban,👳‍♂️;man_white_haired,👨‍🦳;man_with_chinese_cap,👲;man_with_gua_pi_mao,👲;man_with_probing_cane,👨‍🦯;man_with_turban,👳;man_with_veil,👰‍♂️;man_zombie,🧟‍♂️;mango,🥭;mans_shoe,👞;mantlepiece_clock,🕰️;manual_wheelchair,🦽;map,🗺️;maple_leaf,🍁;martial_arts_uniform,🥋;mask,😷;massage,💆;mate,🧉;meat_on_bone,🍖;mechanic,🧑‍🔧;mechanical_arm,🦾;mechanical_leg,🦿;medal,🏅;medical_symbol,⚕️;mega,📣;melon,🍈;melting_face,🫠;memo,📝;men_with_bunny_ears_partying,👯‍♂️;men_wrestling,🤼‍♂️;mending_heart,❤️‍🩹;menorah,🕎;mens,🚹;mermaid,🧜‍♀️;merman,🧜‍♂️;merperson,🧜;metal,🤘;metro,🚇;microbe,🦠;microphone,🎤;microphone2,🎙️;microscope,🔬;middle_finger,🖕;military_helmet,🪖;military_medal,🎖️;milk,🥛;milky_way,🌌;minibus,🚐;minidisc,💽;mirror,🪞;mirror_ball,🪩;mobile_phone,📱;mobile_phone_off,📴;money_mouth,🤑;money_mouth_face,🤑;money_with_wings,💸;moneybag,💰;monkey,🐒;monkey_face,🐵;monorail,🚝;moon_cake,🥮;mortar_board,🎓;mosque,🕌;mosquito,🦟;mother_christmas,🤶;motor_scooter,🛵;motorbike,🛵;motorboat,🛥️;motorcycle,🏍️;motorized_wheelchair,🦼;motorway,🛣️;mount_fuji,🗻;mountain,⛰️;mountain_bicyclist,🚵;mountain_cableway,🚠;mountain_railway,🚞;mountain_snow,🏔️;mouse,🐭;mouse2,🐁;mouse_three_button,🖱️;mouse_trap,🪤;movie_camera,🎥;moyai,🗿;mrs_claus,🤶;muscle,💪;mushroom,🍄;musical_keyboard,🎹;musical_note,🎵;musical_score,🎼;mute,🔇;mx_claus,🧑‍🎄;nail_care,💅;name_badge,📛;national_park,🏞️;nauseated_face,🤢;nazar_amulet,🧿;necktie,👔;negative_squared_cross_mark,❎;nerd,🤓;nerd_face,🤓;nest_with_eggs,🪺;nesting_dolls,🪆;neutral_face,😐;new,🆕;new_moon,🌑;new_moon_with_face,🌚;newspaper,📰;newspaper2,🗞️;next_track,⏭️;ng,🆖;night_with_stars,🌃;nine,9️⃣;ninja,🥷;no_bell,🔕;no_bicycles,🚳;no_entry,⛔;no_entry_sign,🚫;no_good,🙅;no_mobile_phones,📵;no_mouth,😶;no_pedestrians,🚷;no_smoking,🚭;non_potable_water,🚱;nose,👃;notebook,📓;notebook_with_decorative_cover,📔;notepad_spiral,🗒️;notes,🎶;nut_and_bolt,🔩;o,⭕;o2,🅾️;ocean,🌊;octagonal_sign,🛑;octopus,🐙;oden,🍢;office,🏢;office_worker,🧑‍💼;oil,🛢️;oil_drum,🛢️;ok,🆗;ok_hand,👌;old_key,🗝️;older_adult,🧓;older_man,👴;older_woman,👵;olive,🫒;om_symbol,🕉️;on,🔛;oncoming_automobile,🚘;oncoming_bus,🚍;oncoming_police_car,🚔;oncoming_taxi,🚖;one,1️⃣;one_piece_swimsuit,🩱;onion,🧅;open_file_folder,📂;open_hands,👐;open_mouth,😮;ophiuchus,⛎;orange_book,📙;orange_circle,🟠;orange_heart,🧡;orange_square,🟧;orangutan,🦧;orthodox_cross,☦️;otter,🦦;outbox_tray,📤;owl,🦉;ox,🐂;oyster,🦪;package,📦;paella,🥘;page_facing_up,📄;page_with_curl,📃;pager,📟;paintbrush,🖌️;palm_down_hand,🫳;palm_tree,🌴;palm_up_hand,🫴;palms_up_together,🤲;pancakes,🥞;panda_face,🐼;paperclip,📎;paperclips,🖇️;parachute,🪂;park,🏞️;parking,🅿️;parrot,🦜;part_alternation_mark,〽️;partly_sunny,⛅;partying_face,🥳;passenger_ship,🛳️;passport_control,🛂;pause_button,⏸️;paw_prints,🐾;peace,☮️;peace_symbol,☮️;peach,🍑;peacock,🦚;peanuts,🥜;pear,🍐;pen_ballpoint,🖊️;pen_fountain,🖋️;pencil,📝;pencil2,✏️;penguin,🐧;pensive,😔;people_holding_hands,🧑‍🤝‍🧑;people_hugging,🫂;people_with_bunny_ears_partying,👯;people_wrestling,🤼;performing_arts,🎭;persevere,😣;person_bald,🧑‍🦲;person_biking,🚴;person_bouncing_ball,⛹️;person_bowing,🙇;person_climbing,🧗;person_curly_hair,🧑‍🦱;person_doing_cartwheel,🤸;person_facepalming,🤦;person_feeding_baby,🧑‍🍼;person_fencing,🤺;person_frowning,🙍;person_gesturing_no,🙅;person_gesturing_ok,🙆;person_getting_haircut,💇;person_getting_massage,💆;person_golfing,🏌️;person_in_lotus_position,🧘;person_in_manual_wheelchair,🧑‍🦽;person_in_motorized_wheelchair,🧑‍🦼;person_in_steamy_room,🧖;person_in_tuxedo,🤵;person_juggling,🤹;person_kneeling,🧎;person_lifting_weights,🏋️;person_mountain_biking,🚵;person_playing_handball,🤾;person_playing_water_polo,🤽;person_pouting,🙎;person_raising_hand,🙋;person_red_hair,🧑‍🦰;person_rowing_boat,🚣;person_running,🏃;person_shrugging,🤷;person_standing,🧍;person_surfing,🏄;person_swimming,🏊;person_tipping_hand,💁;person_walking,🚶;person_wearing_turban,👳;person_white_hair,🧑‍🦳;person_with_ball,⛹️;person_with_blond_hair,👱;person_with_crown,🫅;person_with_pouting_face,🙎;person_with_probing_cane,🧑‍🦯;person_with_veil,👰;petri_dish,🧫;pick,⛏️;pickup_truck,🛻;pie,🥧;pig,🐷;pig2,🐖;pig_nose,🐽;pill,💊;pilot,🧑‍✈️;pinched_fingers,🤌;pinching_hand,🤏;pineapple,🍍;ping_pong,🏓;pirate_flag,🏴‍☠️;pisces,♓;pizza,🍕;piñata,🪅;placard,🪧;place_of_worship,🛐;play_pause,⏯️;playground_slide,🛝;pleading_face,🥺;plunger,🪠;point_down,👇;point_left,👈;point_right,👉;point_up,☝️;point_up_2,👆;polar_bear,🐻‍❄️;police_car,🚓;police_officer,👮;poo,💩;poodle,🐩;poop,💩;popcorn,🍿;post_office,🏣;postal_horn,📯;postbox,📮;potable_water,🚰;potato,🥔;potted_plant,🪴;pouch,👝;poultry_leg,🍗;pound,💷;pouring_liquid,🫗;pouting_cat,😾;pray,🙏;prayer_beads,📿;pregnant_man,🫃;pregnant_person,🫄;pregnant_woman,🤰;pretzel,🥨;previous_track,⏮️;prince,🤴;princess,👸;printer,🖨️;probing_cane,🦯;projector,📽️;pudding,🍮;punch,👊;purple_circle,🟣;purple_heart,💜;purple_square,🟪;purse,👛;pushpin,📌;put_litter_in_its_place,🚮;question,❓;rabbit,🐰;rabbit2,🐇;raccoon,🦝;race_car,🏎️;racehorse,🐎;racing_car,🏎️;racing_motorcycle,🏍️;radio,📻;radio_button,🔘;radioactive,☢️;radioactive_sign,☢️;rage,😡;railroad_track,🛤️;railway_car,🚃;railway_track,🛤️;rainbow,🌈;rainbow_flag,🏳️‍🌈;raised_back_of_hand,🤚;raised_hand,✋;raised_hand_with_fingers_splayed,🖐️;raised_hand_with_part_between_middle_and_ring_fingers,🖖;raised_hands,🙌;raising_hand,🙋;ram,🐏;ramen,🍜;rat,🐀;razor,🪒;receipt,🧾;record_button,⏺️;recycle,♻️;red_car,🚗;red_circle,🔴;red_envelope,🧧;red_square,🟥;regional_indicator_a,🇦;regional_indicator_b,🇧;regional_indicator_c,🇨;regional_indicator_d,🇩;regional_indicator_e,🇪;regional_indicator_f,🇫;regional_indicator_g,🇬;regional_indicator_h,🇭;regional_indicator_i,🇮;regional_indicator_j,🇯;regional_indicator_k,🇰;regional_indicator_l,🇱;regional_indicator_m,🇲;regional_indicator_n,🇳;regional_indicator_o,🇴;regional_indicator_p,🇵;regional_indicator_q,🇶;regional_indicator_r,🇷;regional_indicator_s,🇸;regional_indicator_t,🇹;regional_indicator_u,🇺;regional_indicator_v,🇻;regional_indicator_w,🇼;regional_indicator_x,🇽;regional_indicator_y,🇾;regional_indicator_z,🇿;registered,®️;relaxed,☺️;relieved,😌;reminder_ribbon,🎗️;repeat,🔁;repeat_one,🔂;restroom,🚻;reversed_hand_with_middle_finger_extended,🖕;revolving_hearts,💞;rewind,⏪;rhino,🦏;rhinoceros,🦏;ribbon,🎀;rice,🍚;rice_ball,🍙;rice_cracker,🍘;rice_scene,🎑;right_anger_bubble,🗯️;right_facing_fist,🤜;right_fist,🤜;rightwards_hand,🫱;ring,💍;ring_buoy,🛟;ringed_planet,🪐;robot,🤖;robot_face,🤖;rock,🪨;rocket,🚀;rofl,🤣;roll_of_paper,🧻;rolled_up_newspaper,🗞️;roller_coaster,🎢;roller_skate,🛼;rolling_eyes,🙄;rolling_on_the_floor_laughing,🤣;rooster,🐓;rose,🌹;rosette,🏵️;rotating_light,🚨;round_pushpin,📍;rowboat,🚣;rugby_football,🏉;runner,🏃;running_shirt_with_sash,🎽;sa,🈂️;safety_pin,🧷;safety_vest,🦺;sagittarius,♐;sailboat,⛵;sake,🍶;salad,🥗;salt,🧂;saluting_face,🫡;sandal,👡;sandwich,🥪;santa,🎅;sari,🥻;satellite,📡;satellite_orbital,🛰️;satisfied,😆;sauropod,🦕;saxophone,🎷;scales,⚖️;scarf,🧣;school,🏫;school_satchel,🎒;scientist,🧑‍🔬;scissors,✂️;scooter,🛴;scorpion,🦂;scorpius,♏;scotland,🏴󠁧󠁢󠁳󠁣󠁴󠁿;scream,😱;scream_cat,🙀;screwdriver,🪛;scroll,📜;seal,🦭;seat,💺;second_place,🥈;second_place_medal,🥈;secret,㊙️;see_no_evil,🙈;seedling,🌱;selfie,🤳;service_dog,🐕‍🦺;seven,7️⃣;sewing_needle,🪡;shaking_hands,🤝;shallow_pan_of_food,🥘;shamrock,☘️;shark,🦈;shaved_ice,🍧;sheep,🐑;shell,🐚;shelled_peanut,🥜;shield,🛡️;shinto_shrine,⛩️;ship,🚢;shirt,👕;shit,💩;shopping_bags,🛍️;shopping_cart,🛒;shopping_trolley,🛒;shorts,🩳;shower,🚿;shrimp,🦐;shrug,🤷;shushing_face,🤫;sick,🤢;sign_of_the_horns,🤘;signal_strength,📶;singer,🧑‍🎤;six,6️⃣;six_pointed_star,🔯;skateboard,🛹;skeleton,💀;ski,🎿;skier,⛷️;skull,💀;skull_and_crossbones,☠️;skull_crossbones,☠️;skunk,🦨;sled,🛷;sleeping,😴;sleeping_accommodation,🛌;sleepy,😪;sleuth_or_spy,🕵️;slight_frown,🙁;slight_smile,🙂;slightly_frowning_face,🙁;slightly_smiling_face,🙂;slot_machine,🎰;sloth,🦥;small_airplane,🛩️;small_blue_diamond,🔹;small_orange_diamond,🔸;small_red_triangle,🔺;small_red_triangle_down,🔻;smile,😄;smile_cat,😸;smiley,😃;smiley_cat,😺;smiling_face_with_3_hearts,🥰;smiling_face_with_tear,🥲;smiling_imp,😈;smirk,😏;smirk_cat,😼;smoking,🚬;snail,🐌;snake,🐍;sneeze,🤧;sneezing_face,🤧;snow_capped_mountain,🏔️;snowboarder,🏂;snowflake,❄️;snowman,⛄;snowman2,☃️;soap,🧼;sob,😭;soccer,⚽;socks,🧦;softball,🥎;soon,🔜;sos,🆘;sound,🔉;space_invader,👾;spades,♠️;spaghetti,🍝;sparkle,❇️;sparkler,🎇;sparkles,✨;sparkling_heart,💖;speak_no_evil,🙊;speaker,🔈;speaking_head,🗣️;speaking_head_in_silhouette,🗣️;speech_balloon,💬;speech_left,🗨️;speedboat,🚤;spider,🕷️;spider_web,🕸️;spiral_calendar_pad,🗓️;spiral_note_pad,🗒️;sponge,🧽;spoon,🥄;sports_medal,🏅;spy,🕵️;squeeze_bottle,🧴;squid,🦑;stadium,🏟️;star,⭐;star2,🌟;star_and_crescent,☪️;star_of_david,✡️;star_struck,🤩;stars,🌠;station,🚉;statue_of_liberty,🗽;steam_locomotive,🚂;stethoscope,🩺;stew,🍲;stop_button,⏹️;stop_sign,🛑;stopwatch,⏱️;straight_ruler,📏;strawberry,🍓;stuck_out_tongue,😛;stuck_out_tongue_closed_eyes,😝;stuck_out_tongue_winking_eye,😜;student,🧑‍🎓;studio_microphone,🎙️;stuffed_flatbread,🥙;stuffed_pita,🥙;sun_with_face,🌞;sunflower,ð»;sunglasses,😎;sunny,☀️;sunrise,🌅;sunrise_over_mountains,🌄;superhero,🦸;supervillain,🦹;surfer,🏄;sushi,🍣;suspension_railway,🚟;swan,🦢;sweat,😓;sweat_drops,💦;sweat_smile,😅;sweet_potato,🍠;swimmer,🏊;symbols,🔣;synagogue,🕍;syringe,💉;t_rex,🦖;table_tennis,🏓;taco,🌮;tada,🎉;takeout_box,🥡;tamale,🫔;tanabata_tree,🎋;tangerine,🍊;taurus,♉;taxi,🚕;tea,🍵;teacher,🧑‍🏫;teapot,🫖;technologist,🧑‍💻;teddy_bear,🧸;telephone,☎️;telephone_receiver,📞;telescope,🔭;tennis,🎾;tent,⛺;test_tube,🧪;thermometer,🌡️;thermometer_face,🤒;thinking,🤔;thinking_face,🤔;third_place,🥉;third_place_medal,🥉;thong_sandal,🩴;thought_balloon,💭;thread,🧵;three,3️⃣;three_button_mouse,🖱️;thumbdown,👎;thumbsdown,👎;thumbsup,👍;thumbup,👍;thunder_cloud_and_rain,⛈️;thunder_cloud_rain,⛈️;ticket,🎫;tickets,🎟️;tiger,🐯;tiger2,🐅;timer,⏲️;timer_clock,⏲️;tired_face,😫;tm,™️;toilet,🚽;tokyo_tower,🗼;tomato,🍅;tongue,👅;toolbox,🧰;tools,🛠️;tooth,🦷;toothbrush,🪥;top,🔝;tophat,🎩;track_next,⏭️;track_previous,⏮️;trackball,🖲️;tractor,🚜;traffic_light,🚥;train,🚋;train2,🚆;tram,🚊;transgender_flag,🏳️‍⚧️;transgender_symbol,⚧;triangular_flag_on_post,🚩;triangular_ruler,📐;trident,🔱;triumph,😤;troll,🧌;trolleybus,🚎;trophy,🏆;tropical_drink,🍹;tropical_fish,🐠;truck,🚚;trumpet,🎺;tulip,🌷;tumbler_glass,🥃;turkey,🦃;turtle,🐢;tv,📺;twisted_rightwards_arrows,🔀;two,2️⃣;two_hearts,💕;two_men_holding_hands,👬;two_women_holding_hands,👭;up,🆙;urn,⚱️;v,✌️;vampire,🧛;vertical_traffic_light,🚦;vhs,📼;vibration_mode,📳;video_camera,📹;video_game,🎮;violin,🎻;virgo,♍;volcano,🌋;volleyball,🏐;vs,🆚;vulcan,🖖;waffle,🧇;wales,🏴󠁧󠁢󠁷󠁬󠁳󠁿;walking,🚶;waning_crescent_moon,🌘;waning_gibbous_moon,🌖;warning,⚠️;wastebasket,🗑️;watch,⌚;water_buffalo,🐃;water_polo,🤽;watermelon,🍉;wave,👋;wavy_dash,〰️;waxing_crescent_moon,🌒;waxing_gibbous_moon,🌔;wc,🚾;weary,😩;wedding,💒;weight_lifter,🏋️;whale,🐳;whale2,🐋;wheel,🛞;wheel_of_dharma,☸️;wheelchair,♿;whisky,🥃;white_check_mark,✅;white_circle,⚪;white_flower,💮;white_frowning_face,☹️;white_heart,🤍;white_large_square,⬜;white_medium_small_square,◽;white_medium_square,◻️;white_small_square,▫️;white_square_button,🔳;white_sun_behind_cloud,🌥️;white_sun_behind_cloud_with_rain,🌦️;white_sun_cloud,🌥️;white_sun_rain_cloud,🌦️;white_sun_small_cloud,🌤️;white_sun_with_small_cloud,🌤️;wilted_flower,🥀;wilted_rose,🥀;wind_blowing_face,🌬️;wind_chime,🎐;window,🪟;wine_glass,🍷;wink,😉;wolf,🐺;woman,👩;woman_artist,👩‍🎨;woman_astronaut,👩‍🚀;woman_bald,👩‍🦲;woman_beard,🧔‍♀️;woman_biking,🚴‍♀️;woman_bouncing_ball,⛹️‍♀️;woman_bowing,🙇‍♀️;woman_cartwheeling,🤸‍♀️;woman_climbing,🧗‍♀️;woman_construction_worker,👷‍♀️;woman_cook,👩‍🍳;woman_curly_haired,👩‍🦱;woman_detective,🕵️‍♀️;woman_elf,🧝‍♀️;woman_facepalming,🤦‍♀️;woman_factory_worker,👩‍🏭;woman_fairy,🧚‍♀️;woman_farmer,👩‍🌾;woman_feeding_baby,👩‍🍼;woman_firefighter,👩‍🚒;woman_frowning,🙍‍♀️;woman_genie,🧞‍♀️;woman_gesturing_no,🙅‍♀️;woman_gesturing_ok,🙆‍♀️;woman_getting_face_massage,💆‍♀️;woman_getting_haircut,💇‍♀️;woman_golfing,🏌️‍♀️;woman_guard,💂‍♀️;woman_health_worker,👩‍⚕️;woman_in_lotus_position,🧘‍♀️;woman_in_manual_wheelchair,👩‍🦽;woman_in_motorized_wheelchair,👩‍🦼;woman_in_steamy_room,🧖‍♀️;woman_in_tuxedo,🤵‍♀️;woman_judge,👩‍⚖️;woman_juggling,🤹‍♀️;woman_kneeling,🧎‍♀️;woman_lifting_weights,🏋️‍♀️;woman_mage,🧙‍♀️;woman_mechanic,👩‍🔧;woman_mountain_biking,🚵‍♀️;woman_office_worker,👩‍💼;woman_pilot,👩‍✈️;woman_playing_handball,🤾‍♀️;woman_playing_water_polo,🤽‍♀️;woman_police_officer,👮‍♀️;woman_pouting,🙎‍♀️;woman_raising_hand,🙋‍♀️;woman_red_haired,👩‍🦰;woman_rowing_boat,🚣‍♀️;woman_running,🏃‍♀️;woman_scientist,👩‍🔬;woman_shrugging,🤷‍♀️;woman_singer,👩‍🎤;woman_standing,🧍‍♀️;woman_student,👩‍🎓;woman_superhero,🦸‍♀️;woman_supervillain,🦹‍♀️;woman_surfing,🏄‍♀️;woman_swimming,🏊‍♀️;woman_teacher,👩‍🏫;woman_technologist,👩‍💻;woman_tipping_hand,💁‍♀️;woman_vampire,🧛‍♀️;woman_walking,🚶‍♀️;woman_wearing_turban,👳‍♀️;woman_white_haired,👩‍🦳;woman_with_headscarf,🧕;woman_with_probing_cane,👩‍🦯;woman_with_veil,👰‍♀️;woman_zombie,🧟‍♀️;womans_clothes,👚;womans_flat_shoe,🥿;womans_hat,👒;women_with_bunny_ears_partying,👯‍♀️;women_wrestling,🤼‍♀️;womens,🚺;wood,🪵;woozy_face,🥴;world_map,🗺️;worm,🪱;worried,😟;worship_symbol,🛐;wrench,🔧;wrestlers,🤼;wrestling,🤼;writing_hand,✍️;x,❌;x_ray,🩻;yarn,🧶;yawning_face,🥱;yellow_circle,🟡;yellow_heart,💛;yellow_square,🟨;yen,💴;yin_yang,☯️;yo_yo,🪀;yum,😋;zany_face,🤪;zap,⚡;zebra,🦓;zero,0️⃣;zipper_mouth,🤐;zipper_mouth_face,🤐;zombie,🧟;zzz,💤"
);


// https://katex.org/docs/supported.html
// agressively "crawled", some are duplicated or not formatted
const SYMBOLS = (function (list) {
    var dict = {};
    for (var i = 0; i < list.length; i++)
        dict[list[i][0]] = list[i][1];
    return dict;
})([
    ['deg', '°'], ['sqrt', '√'], ['cbrt', '∛'], ['der', '∂'], ['cross', '×'], ['left', '←'], ['right', '→'], ['up', '↑'], ['down', '↓'], ['celsius', '℃'], ['fahrenheit', '℉'], ['\\', '\n'],  // overriding latex standard
    ['Alpha', 'A'], ['Beta', 'B'], ['Gamma', 'Γ'], ['Delta', 'Δ'], ['Epsilon', 'E'], ['Zeta', 'Z'], ['Eta', 'H'], ['Theta', 'Θ'], ['Iota', 'I'], ['Kappa', 'K'], ['Lambda', 'Λ'], ['Mu', 'M'], ['Nu', 'N'], ['Xi', 'Ξ'], ['Omicron', 'O'], ['Pi', 'Π'], ['Rho', 'P'], ['Sigma', 'Σ'], ['Tau', 'T'], ['Upsilon', 'Υ'], ['Phi', 'Φ'], ['Chi', 'X'], ['Psi', 'Ψ'], ['Omega', 'Ω'], ['varGamma', 'Γ'], ['varDelta', 'Δ'], ['varTheta', 'Θ'], ['varLambda', 'Λ'], ['varXi', 'Ξ'], ['varPi', 'Π'], ['varSigma', 'Σ'], ['varUpsilon', 'Υ'], ['varPhi', 'Φ'], ['varPsi', 'Ψ'], ['varOmega', 'Ω'], ['alpha', 'α'], ['beta', 'β'], ['gamma', 'γ'], ['delta', 'δ'], ['epsilon', 'ϵ'], ['zeta', 'ζ'], ['eta', 'η'], ['theta', 'θ'], ['iota', 'ι'], ['kappa', 'κ'], ['lambda', 'λ'], ['mu', 'μ'], ['nu', 'ν'], ['xi', 'ξ'], ['omicron', 'ο'], ['pi', 'π'], ['rho', 'ρ'], ['sigma', 'σ'], ['tau', 'τ'], ['upsilon', 'υ'], ['phi', 'φ'], ['chi', 'χ'], ['psi', 'ψ'], ['omega', 'ω'], ['varepsilon', 'ε'], ['varkappa', 'ϰ'], ['vartheta', 'ϑ'], ['thetasym', 'ϑ'], ['varpi', 'ϖ'], ['varrho', 'ϱ'], ['varsigma', 'ς'], ['varphi', 'ϕ'], ['digamma', 'ϝ'],
    ['imath', ''], ['nabla', '∇'], ['Im', 'ℑ'], ['Reals', 'R'], ['jmath', ''], ['partial', '∂'], ['image', 'ℑ'], ['wp', '℘'], ['aleph', 'ℵ'], ['Game', '⅁'], ['Bbbk', 'k'], ['weierp', '℘'], ['alef', 'ℵ'], ['Finv', 'Ⅎ'], ['N', 'N'], ['Z', 'Z'], ['alefsym', 'ℵ'], ['cnums', 'C'], ['natnums', 'N'], ['beth', 'ℶ'], ['Complex', 'C'], ['R', 'R'], ['gimel', 'ℷ'], ['ell', 'ℓ'], ['Re', 'ℜ'], ['daleth', 'ℸ'], ['hbar', 'ℏ'], ['real', 'ℜ'], ['eth', 'ð'], ['hslash', 'ℏ'], ['reals', 'R'],
    ['forall', '∀'], ['complement', '∁'], ['therefore', '∴'], ['emptyset', '∅'], ['exists', '∃'], ['subset', '⊂'], ['because', '∵'], ['empty', '∅'], ['exist', '∃'], ['supset', '⊃'], ['mapsto', '↦'], ['varnothing', '∅'], ['nexists', '∄'], ['mid', '∣'], ['to', '→'], ['implies', '⟹'], ['in', '∈'], ['land', '∧'], ['gets', '←'], ['impliedby', '⟸'], ['isin', '∈'], ['lor', '∨'], ['leftrightarrow', '↔'], ['iff', '⟺'], ['notin', '∉'], ['ni', '∋'], ['notni', '∌'], ['neg', '¬'], ['lnot', '¬'],
    ['sum', '∑'], ['prod', '∏'], ['bigotimes', '⨂'], ['bigvee', '⋁'], ['int', '∫'], ['coprod', '∐'], ['bigoplus', '⨁'], ['bigwedge', '⋀'], ['iint', '∬'], ['intop', '∫'], ['bigodot', '⨀'], ['bigcap', '⋂'], ['iiint', '∭'], ['smallint', '∫'], ['biguplus', '⨄'], ['bigcup', '⋃'], ['oint', '∮'], ['oiint', '∯'], ['oiiint', '∰'], ['bigsqcup', '⨆'],
    ['cdot', '⋅'], ['gtrdot', '⋗'], ['cdotp', '⋅'], ['intercal', '⊺'], ['centerdot', '⋅'], ['land', '∧'], ['rhd', '⊳'], ['circ', '∘'], ['leftthreetimes', '⋋'], ['rightthreetimes', '⋌'], ['amalg', '⨿'], ['circledast', '⊛'], ['ldotp', '.'], ['rtimes', '⋊'], ['And', '&'], ['circledcirc', '⊚'], ['lor', '∨'], ['setminus', '∖'], ['ast', '∗'], ['circleddash', '⊝'], ['lessdot', '⋖'], ['smallsetminus', '∖'], ['barwedge', '⊼'], ['Cup', '⋓'], ['lhd', '⊲'], ['sqcap', '⊓'], ['bigcirc', '◯'], ['cup', '∪'], ['ltimes', '⋉'], ['sqcup', '⊔'], ['bmod', 'mod'], ['curlyvee', '⋎'], ['mod', 'x'], ['xmod', 'xmoda'], ['times', '×'], ['boxdot', '⊡'], ['curlywedge', '⋏'], ['mp', '∓'], ['unlhd', '⊴'], ['boxminus', '⊟'], ['div', '÷'], ['odot', '⊙'], ['unrhd', '⊵'], ['boxplus', '⊞'], ['divideontimes', '⋇'], ['ominus', '⊖'], ['uplus', '⊎'], ['boxtimes', '⊠'], ['dotplus', '∔'], ['oplus', '⊕'], ['vee', '∨'], ['bullet', '∙'], ['doublebarwedge', '⩞'], ['otimes', '⊗'], ['veebar', '⊻'], ['Cap', '⋒'], ['doublecap', '⋒'], ['oslash', '⊘'], ['wedge', '∧'], ['cap', '∩'], ['doublecup', '⋓'], ['pm', '±'], ['wr', '≀'],
    ['eqcirc', '≖'], ['lesseqgtr', '⋚'], ['sqsupset', '⊐'], ['eqcolon', '−:'], ['lesseqqgtr', '⪋'], ['sqsupseteq', '⊒'], ['Eqcolon', '−::'], ['lessgtr', '≶'], ['Subset', '⋐'], ['eqqcolon', '=:'], ['lesssim', '≲'], ['subset', '⊂'], ['sub', '⊂'], ['approx', '≈'], ['Eqqcolon', '=::'], ['ll', '≪'], ['approxeq', '≊'], ['eqsim', '≂'], ['lll', '⋘'], ['subseteqq', '⫅'], ['asymp', '≍'], ['eqslantgtr', '⪖'], ['llless', '⋘'], ['succ', '≻'], ['backepsilon', '∍'], ['eqslantless', '⪕'], ['lt', '<'], ['succapprox', '⪸'], ['backsim', '∽'], ['equiv', '≡'], ['mid', '∣'], ['succcurlyeq', '≽'], ['backsimeq', '⋍'], ['fallingdotseq', '≒'], ['models', '⊨'], ['succeq', '⪰'], ['between', '≬'], ['frown', '⌢'], ['multimap', '⊸'], ['succsim', '≿'], ['bowtie', '⋈'], ['ge', '≥'], ['owns', '∋'], ['Supset', '⋑'], ['bumpeq', '≏'], ['geq', '≥'], ['parallel', '∥'], ['supset', '⊃'], ['Bumpeq', '≎'], ['geqq', '≧'], ['perp', '⊥'], ['supseteq', '⊇'], ['supe', '⊇'], ['circeq', '≗'], ['geqslant', '⩾'], ['pitchfork', '⋔'], ['supseteqq', '⫆'], ['colonapprox', ':≈'], ['gg', '≫'], ['prec', '≺'], ['thickapprox', '≈'], ['Colonapprox', '::≈'], ['ggg', '⋙'], ['precapprox', '⪷'], ['thicksim', '∼'], ['coloneq', ':−'], ['gggtr', '⋙'], ['preccurlyeq', '≼'], ['trianglelefteq', '⊴'], ['Coloneq', '::−'], ['gt', '>'], ['preceq', '⪯'], ['triangleq', '≜'], ['coloneqq', ':='], ['gtrapprox', '⪆'], ['precsim', '≾'], ['trianglerighteq', '⊵'], ['Coloneqq', '::='], ['gtreqless', '⋛'], ['propto', '∝'], ['varpropto', '∝'], ['colonsim', ':∼'], ['gtreqqless', '⪌'], ['risingdotseq', '≓'], ['vartriangle', '△'], ['Colonsim', '::∼'], ['gtrless', '≷'], ['shortmid', '∣'], ['vartriangleleft', '⊲'], ['cong', '≅'], ['gtrsim', '≳'], ['shortparallel', '∥'], ['vartriangleright', '⊳'], ['curlyeqprec', '⋞'], ['in', '∈'], ['isin', '∈'], ['sim', '∼'], ['vcentcolon', ':'], ['curlyeqsucc', '⋟'], ['Join', '⋈'], ['simeq', '≃'], ['vdash', '⊢'], ['dashv', '⊣'], ['le', '≤'], ['smallfrown', '⌢'], ['vDash', '⊨'], ['dblcolon', '::'], ['leq', '≤'], ['smallsmile', '⌣'], ['Vdash', '⊩'], ['doteq', '≐'], ['leqq', '≦'], ['smile', '⌣'], ['Vvdash', '⊪'], ['Doteq', '≑'], ['leqslant', '⩽'], ['sqsubset', '⊏'], ['doteqdot', '≑'], ['lessapprox', '⪅'], ['sqsubseteq', '⊑'],
    ['gnapprox', '⪊'], ['ngeqslant', ''], ['nsubseteq', '⊈'], ['precneqq', '⪵'], ['gneq', '⪈'], ['ngtr', '≯'], ['nsubseteqq', ''], ['precnsim', '⋨'], ['gneqq', '≩'], ['nleq', '≰'], ['nsucc', '⊁'], ['subsetneq', '⊊'], ['gnsim', '⋧'], ['nleqq', ''], ['nsucceq', '⋡'], ['subsetneqq', '⫋'], ['gvertneqq', ''], ['nleqslant', ''], ['nsupseteq', '⊉'], ['succnapprox', '⪺'], ['lnapprox', '⪉'], ['nless', '≮'], ['nsupseteqq', ''], ['succneqq', '⪶'], ['lneq', '⪇'], ['nmid', '∤'], ['ntriangleleft', '⋪'], ['succnsim', '⋩'], ['lneqq', '≨'], ['ntrianglelefteq', '⋬'], ['supsetneq', '⊋'], ['lnsim', '⋦'], ['notni', '∌'], ['ntriangleright', '⋫'], ['supsetneqq', '⫌'], ['lvertneqq', ''], ['nparallel', '∦'], ['ntrianglerighteq', '⋭'], ['varsubsetneq', ''], ['ncong', '≆'], ['nprec', '⊀'], ['nvdash', '⊬'], ['varsubsetneqq', ''], ['ne', '≠'], ['npreceq', '⋠'], ['nvDash', '⊭'], ['varsupsetneq', ''], ['neq', '≠'], ['nshortmid', ''], ['nVDash', '⊯'], ['varsupsetneqq', ''], ['ngeq', '≱'], ['nshortparallel', ''], ['nVdash', '⊮'], ['ngeqq', ''], ['nsim', '≁'], ['precnapprox', '⪹'], ['circlearrowleft', '↺'], ['leftharpoonup', '↼'], ['rArr', '⇒'], ['circlearrowright', '↻'], ['leftleftarrows', '⇇'], ['rarr', '→'], ['curvearrowleft', '↶'], ['leftrightarrow', '↔'], ['restriction', '↾'], ['curvearrowright', '↷'], ['Leftrightarrow', '⇔'], ['rightarrow', '→'], ['Darr', '⇓'], ['leftrightarrows', '⇆'], ['Rightarrow', '⇒'], ['dArr', '⇓'], ['leftrightharpoons', '⇋'], ['rightarrowtail', '↣'], ['darr', '↓'], ['leftrightsquigarrow', '↭'], ['rightharpoondown', '⇁'], ['dashleftarrow', '⇠'], ['Lleftarrow', '⇚'], ['rightharpoonup', '⇀'], ['dashrightarrow', '⇢'], ['longleftarrow', '⟵'], ['rightleftarrows', '⇄'], ['downarrow', '↓'], ['Longleftarrow', '⟸'], ['rightleftharpoons', '⇌'], ['Downarrow', '⇓'], ['longleftrightarrow', '⟷'], ['rightrightarrows', '⇉'], ['downdownarrows', '⇊'], ['Longleftrightarrow', '⟺'], ['rightsquigarrow', '⇝'], ['downharpoonleft', '⇃'], ['longmapsto', '⟼'], ['Rrightarrow', '⇛'], ['downharpoonright', '⇂'], ['longrightarrow', '⟶'], ['Rsh', '↱'], ['gets', '←'], ['Longrightarrow', '⟹'], ['searrow', '↘'], ['Harr', '⇔'], ['looparrowleft', '↫'], ['swarrow', '↙'], ['hArr', '⇔'], ['looparrowright', '↬'], ['to', '→'], ['harr', '↔'], ['Lrarr', '⇔'], ['twoheadleftarrow', '↞'], ['hookleftarrow', '↩'], ['lrArr', '⇔'], ['twoheadrightarrow', '↠'], ['hookrightarrow', '↪'], ['lrarr', '↔'], ['Uarr', '⇑'], ['iff', '⟺'], ['Lsh', '↰'], ['uArr', '⇑'], ['impliedby', '⟸'], ['mapsto', '↦'], ['uarr', '↑'], ['implies', '⟹'], ['nearrow', '↗'], ['uparrow', '↑'], ['Larr', '⇐'], ['nleftarrow', '↚'], ['Uparrow', '⇑'], ['lArr', '⇐'], ['nLeftarrow', '⇍'], ['updownarrow', '↕'], ['larr', '←'], ['nleftrightarrow', '↮'], ['Updownarrow', '⇕'], ['leadsto', '⇝'], ['nLeftrightarrow', '⇎'], ['upharpoonleft', '↿'], ['leftarrow', '←'], ['nrightarrow', '↛'], ['upharpoonright', '↾'], ['Leftarrow', '⇐'], ['nRightarrow', '⇏'], ['upuparrows', '⇈'], ['leftarrowtail', '↢'], ['nwarrow', '↖'], ['leftharpoondown', '↽'], ['Rarr', '⇒'],
    ['dots', '…'], ['%', '%'], ['cdots', '⋯'], ['#', '#'], ['ddots', '⋱'], ['&', '&'], ['ldots', '…'], ['nabla', '∇'], ['_', '_'], ['vdots', '⋮'], ['infty', '∞'], ['dotsb', '⋯'], ['infin', '∞'], ['text{--}', '–'], ['dotsc', '…'], ['checkmark', '✓'], ['dotsi', '⋯'], ['dag', '†'], ['text{---}', '—'], ['dotsm', '⋯'], ['dagger', '†'], ['dotso', '…'], ['sdot', '⋅'], ['ddag', '‡'], ['mathellipsis', '…'], ['ddagger', '‡'], ['text{textquoteleft}', '‘'], ['Box', '□'], ['Dagger', '‡'], ['lq', '‘'], ['square', '□'], ['angle', '∠'], ['blacksquare', '■'], ['measuredangle', '∡'], ['triangle', '△'], ['sphericalangle', '∢'], ['triangledown', '▽'], ['top', '⊤'], ['triangleleft', '◃'], ['bot', '⊥'], ['triangleright', '▹'], ['$', '$'], ['colon', ':'], ['bigtriangledown', '▽'], ['backprime', '‵'], ['bigtriangleup', '△'], ['pounds', '£'], ['prime', '′'], ['blacktriangle', '▲'], ['mathsterling', '£'], ['blacktriangledown', '▼'], ['blacktriangleleft', '◀'], ['yen', '¥'], ['blacktriangleright', '▶'], ['surd', '√'], ['diamond', '⋄'], ['degree', '°'], ['Diamond', '◊'], ['lozenge', '◊'], ['mho', '℧'], ['blacklozenge', '⧫'], ['diagdown', '╲'], ['star', '⋆'], ['diagup', '╱'], ['bigstar', '★'], ['flat', '♭'], ['clubsuit', '♣'], ['natural', '♮'], ['clubs', '♣'], ['sharp', '♯'], ['circledR', '®'], ['diamondsuit', '♢'], ['heartsuit', '♡'], ['diamonds', '♢'], ['hearts', '♡'], ['circledS', 'Ⓢ'], ['spadesuit', '♠'], ['spades', '♠'], ['maltese', '✠'], ['minuso', '−'],
]);

// superscripts and subscripts
const SUBASES = "0123456789abcdefghijklmnoprstuvwxyzABDEGHIJKLMNOPRTUVWβγδϵθιψφϕχ+-=(/)∫";
const SUPSCPT = "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻᴬᴮᴰᴱᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿᵀᵁⱽᵂᵝᵞᵟᵋᶿᶥᵠᵠᵠᵡ⁺⁻⁼⁽ᐟ⁾ᶴ";
const SUBSCPT = "₀₁₂₃₄₅₆₇₈₉ₐbcdₑfgₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥwₓyzABDEGHIJKLMNOPRTUVWᵦᵧδϵθιᵩᵩᵩᵪ₊₋₌₍/₎ʃ";

// https://www.unicode.org/charts/PDF/U0300.pdf
// https://www.unicode.org/charts/PDF/U20D0.pdf
const ACCENTS = {
    "acute": "\u0301",
    "bar": "\u0304",
    "breve": "\u0306",
    "check": "\u030c",
    "dot": "\u0307",
    "ddot": "\u0308",
    "grave": "\u0300",
    "hat": "\u0302",
    "tilde": "\u0303",
    "vec": "\u20d7",
    "overleftarrow": "\u20d6",
    "underleftarrow": "\u20ee",
    "overleftharpoon": "\u20d0",
    "overleftrightarrow": "\u20e1",
    "overline": "\u0305",
    "underline": "\u0332",
    "mathring": "\u030a",
    "overrightarrow": "\u20d7",
    "underrightarrow": "\u20ef",
    "overrightharpoon": "\u20d1",
    "underbar": "\u0331"
};


function replaceEmojis(str) {
    var res = "";
    for (var i = 0; i < str.length; i++) {
        if (str[i] != ':' || (i > 0 && str[i - 1] == '\\')) {
            res += str[i];
            continue;
        }
        var j;
        for (j = i + 1; j < str.length; j++) {
            if (str[j] == ':') break;
        }
        if (j == str.length) {
            res += str.substring(i, j);
            break;
        }
        var between = str.substring(i, j + 1);
        var emoji = between.replace(/\:/g, '').toLowerCase();
        if (EMOJIS.hasOwnProperty(emoji))
            between = EMOJIS[emoji];
        res += between;
        i = j;
    }
    return res;
}


function replaceSymbols(arr) {
    for (var i = 1; i < arr.length; i++) {
        if (arr[i - 1] == '\\') {
            if (SYMBOLS.hasOwnProperty(arr[i])) {
                arr[i - 1] = '';
                arr[i] = SYMBOLS[arr[i]];
            }
            if (/^[0-9A-Za-z]+$/.test(arr[i]) &&
                !ACCENTS.hasOwnProperty(arr[i])) {
                arr[i - 1] = '';
            }
        }
    }
    return arr;
}


function replaceSuperSubscript(arr) {
    function toSup(s) {
        var t = "";
        for (var i = 0; i < s.length; i++) {
            var d = SUBASES.indexOf(s[i]);
            if (d == -1 || s[i] == SUPSCPT[d]) return s;
            t += SUPSCPT[d];
        };
        return t;
    };
    function toSub(s) {
        var t = "";
        for (var i = 0; i < s.length; i++) {
            var d = SUBASES.indexOf(s[i]);
            if (d == -1 || s[i] == SUBSCPT[d]) return s;
            t += SUBSCPT[d];
        };
        return t;
    }
    for (var i = 0; i < arr.length - 1; i++) {
        if (!(arr[i] == '^' || arr[i] == '_')) continue;
        var remapper = arr[i] == '^' ? toSup : toSub;
        if (arr[i + 1] == '{') {  // brackets
            var converted = [], success = true;
            var i0 = i, stack = 1;
            for (i += 2; i < arr.length && arr[i] != '\n'; i++) {
                if (arr[i - 1] != '\\') {
                    // shouldn't matter because
                    // curly brackets are not in the list
                    if (arr[i] == '{') {
                        stack++;
                        arr[i] = '';
                        continue;
                    }
                    if (arr[i] == '}') {
                        stack--;
                        if (stack == 0) break;
                        else arr[i] = '';
                        continue;
                    }
                }
                if (arr[i] == arr[i0]) {
                    converted.push('');
                    continue;
                }
                var s = remapper(arr[i]);
                if (s == arr[i]) {
                    success = false;
                    break;
                }
                else converted.push(s);
            }
            var i1 = i;
            if (success) {
                arr[i0] = arr[i0 + 1] = '';
                i0 += 2;
                for (var i = i0; i < i1; i++)
                    arr[i] = converted[i - i0];
                if (i < arr.length && arr[i] == '}')
                    arr[i] = '';
            }
        }
        else {  // one word
            var s = remapper(arr[i + 1]);
            if (s != arr[i + 1])
                arr[i] = '', arr[i + 1] = s;
        }
    }
    return arr;
}


function replaceAccents(arr) {
    for (var i = 1; i < arr.length - 1; i++) {
        if (arr[i - 1] != '\\' || arr[i + 1] != '{'
            || !ACCENTS.hasOwnProperty(arr[i]))
            continue;
        var accent = ACCENTS[arr[i]];
        var stack = 1;
        arr[i - 1] = arr[i] = arr[i + 1] = '';
        var i0 = i;
        for (i += 2; i < arr.length; i++) {
            if (arr[i] == '{') stack += 1;
            if (arr[i] == '}') stack -= 1;
            if (stack == 0) {
                arr[i] = '';
                i--; break;
            }
            if (/^[A-Za-z0-9\u0370-\u03ff\u0300-\u036F\u20D0-\u20FF]+$/.test(arr[i]) &&
                !(SYMBOLS.hasOwnProperty(arr[i]) || ACCENTS.hasOwnProperty(arr[i]))) {
                var s = arr[i], t = "";
                for (var j = 0; j < s.length; j++) {
                    t += s[j];
                    if (/[A-Za-z0-9\u0370-\u03ff]/.test(s[j])) t += accent;
                }
                t = s + accent;
                arr[i] = t;
            }
        }
        i = i0 + 1;
    }
    return arr;
}


function formatPlainText(src) {
    // split to array
    src = src.replace(/\r/g, '');
    src = src.replace(/\s+$/g, '');
    src = replaceEmojis(src);
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
    if (/[A-Za-z0-9]$/.test(src) && st != "") arr.push(st);
    // console.log(arr);

    arr = replaceSymbols(arr).filter(function (e) { return e != ''; });
    arr = replaceSuperSubscript(arr).filter(function (e) { return e != ''; });
    arr = replaceAccents(arr).filter(function (e) { return e != ''; });

    return arr.join('').replace(/\s+$/, '');
}


// Search command
function searchDict(formatter, dict, keyword) {
    var result = [];
    keyword = keyword.split(' ');
    for (var key in dict) {
        if (!dict.hasOwnProperty(key)) continue;
        var match = true;
        for (var i = 0; i < keyword.length; i++) {
            if (key.search(keyword[i]) == -1) match = false;
        }
        if (match) {
            var formatted = formatter.replace("{key}", key).replaceAll("{char}", dict[key]);
            result.push(formatted);
        }
    }
    return result
}
function searchCommand(keyword) {
    var commands = [];
    var rawKeyword = keyword.replace(/[^\w]/g, ' ').trim();
    if (!/\\/.test(keyword) || /\:/.test(keyword)) {
        var emojis = searchDict(":{key}: {char}", EMOJIS, rawKeyword);
        commands = commands.concat(emojis);
    }
    if (!/\:/.test(keyword) || /\\/.test(keyword)) {
        var symbols = searchDict("\\{key} {char}", SYMBOLS, rawKeyword);
        // var accents = searchDict("\\{key} \u25cc{char}", ACCENTS, rawKeyword);
        var accents = searchDict("\\{key} a{char}b{char}c{char}", ACCENTS, rawKeyword);
        commands = commands.concat(symbols).concat(accents);
    }
    let comp = (s) => s.replace(/^[^\w]/g, '').toLowerCase();
    commands.sort((a, b) => comp(a) > comp(b) ? 1 : -1);
    return commands;
}
