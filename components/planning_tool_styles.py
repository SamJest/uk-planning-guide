STRUCTURED_TOOL_STYLES = """
.decision-engine-card{padding:0;background:linear-gradient(180deg,rgba(255,255,255,.98),rgba(247,241,232,.94)),linear-gradient(135deg,rgba(31,111,95,.06),transparent 58%);border-color:rgba(31,111,95,.16);overflow:hidden;}
.decision-engine{min-width:0;max-width:100%;padding:0;overflow-wrap:normal;word-break:normal;}
.decision-shell-desktop{display:block;}
.decision-shell-mobile{display:none;}
.decision-desktop-shell{padding:30px;}
.decision-engine-header{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;margin-bottom:24px;}
.decision-engine-header > div{min-width:0;}
.decision-engine-header h2{margin-bottom:10px;}
.decision-kicker{display:inline-flex;align-items:center;padding:8px 12px;margin-bottom:12px;border-radius:999px;background:rgba(31,111,95,.10);color:var(--accent-text);font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;box-shadow:inset 0 0 0 1px rgba(31,111,95,.08);}
.decision-header-actions{display:flex;gap:10px;flex:0 1 auto;flex-wrap:wrap;justify-content:flex-end;align-items:flex-start;min-width:0;}
.decision-trust-note{display:grid;gap:6px;margin-top:14px;padding:14px 15px;background:rgba(223,241,234,.54);border:1px solid rgba(31,111,95,.12);border-radius:16px;}
.decision-trust-note strong{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--accent-text);}
.decision-trust-note span{font-size:14px;line-height:1.58;color:var(--ink-soft);}
.decision-progress{margin-bottom:24px;padding:18px 18px 16px;background:rgba(255,255,255,.82);border:1px solid rgba(31,41,55,.08);border-radius:20px;box-shadow:var(--shadow-soft);overflow:hidden;}
.decision-progress-top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap;margin-bottom:14px;}
.decision-progress-top strong{font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);}
.decision-progress-top span{font-size:14px;line-height:1.5;color:var(--ink-faint);}
.decision-progress-bar{height:8px;border-radius:999px;background:rgba(31,41,55,.08);overflow:hidden;margin-bottom:16px;}
.decision-progress-bar span{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,var(--accent),#2b8a78);transition:width .25s ease;}
.decision-step-labels{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));}
.decision-step-label{display:flex;flex-direction:column;gap:5px;min-width:0;padding:11px 13px;border-radius:16px;background:rgba(247,241,232,.76);border:1px solid rgba(31,41,55,.06);transition:border-color .18s ease, box-shadow .18s ease, background-color .18s ease;}
.decision-step-label.active{background:rgba(223,241,234,.94);border-color:rgba(31,111,95,.22);box-shadow:0 12px 24px rgba(31,111,95,.10);}
.decision-step-label.done{background:rgba(31,111,95,.08);}
.decision-step-number{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-faint);}
.decision-step-name{font-size:14px;font-weight:700;color:var(--ink);}
.decision-layout{display:grid;gap:18px;grid-template-columns:minmax(0,1.35fr) minmax(0,.85fr);align-items:start;}
.decision-panel,.decision-sidebar{min-width:0;padding:22px;background:rgba(255,255,255,.84);border:1px solid rgba(31,41,55,.08);border-radius:22px;box-shadow:var(--shadow-soft);}
.decision-sidebar{position:sticky;top:92px;}
.decision-mobile-calculator-shell{display:grid;gap:20px;padding:30px;}
.decision-mobile-calculator-header{display:grid;gap:14px;padding:0 0 6px;}
.decision-mobile-calculator-header h2{margin-bottom:0;}
.decision-mobile-calculator-actions{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-start;}
.decision-mobile-calculator-body{display:grid;gap:18px;}
.decision-mobile-calculator-panel,.decision-mobile-calculator-summary{min-width:0;padding:22px;background:rgba(255,255,255,.84);border:1px solid rgba(31,41,55,.08);border-radius:22px;box-shadow:var(--shadow-soft);}
.decision-mobile-calculator-panel{display:grid;gap:18px;}
.decision-mobile-calculator-summary{display:grid;gap:14px;background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(247,241,232,.86));}
.decision-mobile-calculator-summary h3{margin:0;}
.decision-mobile-calculator-step-intro{display:grid;gap:8px;padding:16px 18px;background:linear-gradient(135deg,rgba(247,241,232,.74),rgba(255,255,255,.94));border:1px solid rgba(31,41,55,.06);border-radius:18px;}
.decision-mobile-calculator-step-intro strong{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent-text);}
.decision-mobile-calculator-step-intro p{margin:0;color:var(--ink-soft);}
.decision-step-copy{min-width:0;margin-bottom:20px;padding:18px 18px 16px;background:linear-gradient(135deg,rgba(247,241,232,.68),rgba(255,255,255,.92));border:1px solid rgba(31,41,55,.06);border-radius:18px;}
.decision-step-copy h3{margin-bottom:8px;}
.decision-question,.decision-result{min-width:0;}
.decision-question{padding:18px;background:rgba(255,255,255,.62);border:1px solid rgba(31,41,55,.06);border-radius:18px;}
.decision-question h4,.decision-result h3,.decision-panel h3,.decision-sidebar h3{overflow-wrap:anywhere;}
.decision-question h4{margin-bottom:12px;font-size:1.02rem;}
.decision-choice-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));}
.decision-binary-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));margin-top:18px;}
.decision-question + .decision-question{margin-top:20px;}
.decision-choice{width:100%;min-width:0;min-height:64px;padding:17px 16px 16px;text-align:left;background:rgba(255,255,255,.94);border:1px solid rgba(31,41,55,.12);border-radius:18px;box-shadow:none;color:var(--ink);transition:border-color .18s ease, box-shadow .18s ease, transform .18s ease, background-color .18s ease;}
.decision-choice:hover{background:#fff;border-color:rgba(31,111,95,.28);box-shadow:0 14px 26px rgba(31,41,55,.08);}
.decision-choice:focus-visible,.decision-chip:focus-visible,.decision-result-link:focus-visible,.tool-fallback-link:focus-visible,.explorer-link:focus-visible{outline:3px solid rgba(31,111,95,.18);outline-offset:2px;border-color:rgba(31,111,95,.34);}
.decision-choice.selected{background:linear-gradient(135deg,rgba(223,241,234,.96),rgba(255,255,255,.98));border-color:rgba(31,111,95,.34);box-shadow:0 16px 28px rgba(31,111,95,.12);}
.decision-choice strong{display:block;margin-bottom:6px;font-size:15px;line-height:1.32;}
.decision-choice span{display:block;font-size:13px;line-height:1.58;color:var(--ink-soft);}
.decision-chip-row{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));}
.decision-chip{width:100%;min-width:0;min-height:48px;padding:11px 14px;border-radius:999px;background:#fff;border:1px solid rgba(31,41,55,.12);color:var(--ink);font-size:14px;font-weight:700;box-shadow:none;transition:border-color .18s ease, box-shadow .18s ease, background-color .18s ease;}
.decision-chip:hover{border-color:rgba(31,111,95,.24);}
.decision-chip:active,.decision-choice:active,.decision-result-link:active,.tool-fallback-link:active,.explorer-link:active{transform:translateY(0);}
.decision-chip.selected{background:rgba(223,241,234,.92);border-color:rgba(31,111,95,.28);color:var(--accent-text);box-shadow:0 10px 18px rgba(31,111,95,.10);}
.decision-question-note{margin-top:10px;font-size:13px;line-height:1.55;color:var(--ink-faint);}
.decision-review-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));}
.decision-review-card{min-width:0;padding:15px 16px;background:rgba(247,241,232,.76);border:1px solid rgba(31,41,55,.08);border-radius:18px;}
.decision-review-card strong{display:block;margin-bottom:4px;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-faint);}
.decision-nav{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-top:24px;padding-top:18px;border-top:1px solid rgba(31,41,55,.08);flex-wrap:wrap;}
.decision-nav .cta,.decision-nav .button-secondary{min-height:48px;margin:0;}
.decision-loading{display:flex;flex-direction:column;align-items:flex-start;gap:12px;padding:28px 24px;background:linear-gradient(135deg,rgba(223,241,234,.95),rgba(255,255,255,.95));border:1px solid rgba(31,111,95,.16);border-radius:22px;box-shadow:var(--shadow-soft);}
.decision-loading-dots{display:inline-flex;gap:8px;}
.decision-loading-dots span{width:10px;height:10px;border-radius:999px;background:rgba(31,111,95,.28);animation:decisionPulse 1s infinite ease-in-out;}
.decision-loading-dots span:nth-child(2){animation-delay:.12s;}
.decision-loading-dots span:nth-child(3){animation-delay:.24s;}
@keyframes decisionPulse{0%,80%,100%{transform:scale(.8);opacity:.45;}40%{transform:scale(1);opacity:1;}}
.decision-result{display:grid;gap:18px;}
.decision-result-banner{position:relative;padding:22px;border-radius:22px;border:1px solid rgba(31,41,55,.08);box-shadow:var(--shadow-soft);}
.decision-result-banner.good{background:linear-gradient(135deg,rgba(223,241,234,.98),rgba(255,255,255,.95));border-color:rgba(31,111,95,.18);}
.decision-result-banner.warn{background:linear-gradient(135deg,rgba(255,246,228,.98),rgba(255,255,255,.95));border-color:rgba(183,121,31,.22);}
.decision-result-banner.danger{background:linear-gradient(135deg,rgba(255,236,233,.98),rgba(255,255,255,.95));border-color:rgba(186,66,55,.22);}
.decision-result-banner.info{background:linear-gradient(135deg,rgba(234,243,250,.98),rgba(255,255,255,.95));border-color:rgba(69,117,160,.22);}
.decision-result-banner h3{margin-bottom:10px;font-size:clamp(1.42rem,2.4vw,1.9rem);line-height:1.08;}
.decision-result-banner p{max-width:60ch;font-size:15px;line-height:1.68;color:var(--ink-soft);}
.decision-status{display:inline-flex;align-items:center;padding:9px 13px;border-radius:999px;margin-bottom:12px;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;background:rgba(255,255,255,.88);color:var(--ink);box-shadow:inset 0 0 0 1px rgba(31,41,55,.06),0 10px 18px rgba(31,41,55,.06);}
.decision-result-grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));}
.decision-result-card{min-width:0;padding:18px;background:rgba(255,255,255,.88);border:1px solid rgba(31,41,55,.08);border-radius:18px;box-shadow:var(--shadow-soft);}
.decision-result-card h3{margin-bottom:8px;}
.decision-result-card ul{padding-left:18px;}
.decision-result-links{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));}
.decision-result-link{display:block;min-width:0;padding:16px;background:rgba(255,255,255,.92);border:1px solid rgba(31,41,55,.08);border-radius:18px;color:inherit;box-shadow:var(--shadow-soft);}
.decision-result-link:hover{border-color:rgba(31,111,95,.22);box-shadow:0 18px 30px rgba(31,41,55,.08);transform:translateY(-1px);}
.decision-result-link strong{display:block;margin-bottom:6px;}
.decision-follow-up{display:grid;gap:14px;margin-top:10px;}
.decision-follow-up-card{display:grid;gap:14px;padding:18px;background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(247,241,232,.86));border:1px solid rgba(31,41,55,.08);border-radius:20px;box-shadow:var(--shadow-soft);}
.decision-follow-up-heading{display:grid;gap:6px;}
.decision-follow-up-heading h3{margin-bottom:0;}
.decision-follow-up-heading p{margin:0;line-height:1.6;color:var(--ink-soft);}
.decision-follow-up-kicker{display:inline-flex;align-items:center;width:max-content;padding:7px 10px;border-radius:999px;background:rgba(31,111,95,.10);color:var(--accent-text);font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;}
.decision-follow-up-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));}
.decision-follow-up-link{display:block;min-width:0;padding:16px;background:rgba(255,255,255,.94);border:1px solid rgba(31,41,55,.08);border-radius:18px;color:inherit;box-shadow:var(--shadow-soft);}
.decision-follow-up-link:hover{border-color:rgba(31,111,95,.22);box-shadow:0 18px 30px rgba(31,41,55,.08);transform:translateY(-1px);}
.decision-follow-up-link strong{display:block;margin-bottom:6px;}
.decision-follow-up-link span{display:block;font-size:14px;line-height:1.58;color:var(--ink-soft);}
.decision-email-capture{display:grid;gap:10px;grid-template-columns:minmax(0,1fr) auto;align-items:center;}
.decision-email-input{width:100%;min-width:0;min-height:50px;padding:13px 15px;border:1px solid rgba(31,41,55,.14);border-radius:16px;background:#fff;color:var(--ink);}
.decision-email-button{min-height:50px;padding:14px 20px;}
.decision-email-note{grid-column:1 / -1;margin:0;font-size:13px;line-height:1.55;color:var(--ink-faint);}
.decision-inline-note{padding:14px 15px;background:rgba(223,241,234,.54);border:1px solid rgba(31,111,95,.12);border-radius:16px;font-size:14px;line-height:1.58;color:var(--ink-soft);}
.decision-sidebar h3{margin-bottom:10px;}
.decision-summary-list{display:grid;gap:10px;margin-bottom:18px;}
.decision-summary-item{min-width:0;padding:12px 14px;background:rgba(247,241,232,.74);border:1px solid rgba(31,41,55,.08);border-radius:16px;}
.decision-summary-item strong{display:block;margin-bottom:4px;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-faint);}
.decision-method-note{padding:14px 15px;background:rgba(223,241,234,.62);border:1px solid rgba(31,111,95,.12);border-radius:16px;font-size:14px;color:var(--ink-soft);}
.tool-fallback{display:grid;gap:14px;padding:22px;background:linear-gradient(135deg,rgba(247,241,232,.9),rgba(255,255,255,.96));border:1px solid rgba(31,41,55,.08);border-radius:22px;}
.tool-fallback h3{margin-bottom:0;}
.tool-fallback-links{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));}
.tool-fallback-link{display:block;min-width:0;padding:16px;background:rgba(255,255,255,.92);border:1px solid rgba(31,41,55,.08);border-radius:18px;color:inherit;box-shadow:var(--shadow-soft);}
.tool-fallback-link:hover{border-color:rgba(31,111,95,.22);box-shadow:0 18px 30px rgba(31,41,55,.08);transform:translateY(-1px);}
.tool-fallback-link strong{display:block;margin-bottom:6px;}
.decision-step-number,.decision-step-name,.decision-choice strong,.decision-choice span,.decision-summary-item span,.decision-review-card span,.decision-result-link span,.decision-result-card li,.decision-method-note,.tool-fallback p,.explorer-fit-note,.explorer-status{writing-mode:horizontal-tb;text-orientation:mixed;white-space:normal;word-break:normal;overflow-wrap:anywhere;hyphens:none;}
@media (max-width:960px){.decision-engine-card{overflow:visible;}.decision-engine{overflow-x:hidden;}.decision-desktop-shell{padding:22px;}.decision-engine-header{flex-direction:column;align-items:stretch;gap:14px;}.decision-header-actions{justify-content:flex-start;}.decision-layout{grid-template-columns:1fr !important;}.decision-sidebar{position:static;max-width:100%;width:100%;margin-top:12px;}.decision-panel,.decision-sidebar{max-width:100%;width:100%;}.decision-step-labels{grid-template-columns:repeat(2,minmax(0,1fr));}.decision-mobile-calculator-shell{padding:22px;}}
@media (max-width:767px){.decision-shell-desktop{display:none !important;}.decision-shell-mobile{display:block !important;}.decision-mobile-calculator-shell{padding:18px;gap:14px;}.decision-mobile-calculator-actions{display:grid;gap:10px;}.decision-mobile-calculator-actions > *{width:100%;min-height:48px;margin:0;}.decision-mobile-calculator-panel,.decision-mobile-calculator-summary,.decision-follow-up-card{padding:18px;border-radius:20px;}.decision-mobile-calculator-step-intro{padding:15px 16px;}.decision-trust-note{margin-top:12px;}.decision-step-labels{gap:8px;grid-template-columns:1fr !important;}.decision-step-label{display:block;padding:12px 14px;max-width:100%;width:100%;}.decision-step-number,.decision-step-name{display:block;max-width:100%;line-height:1.25;}.decision-choice-grid,.decision-binary-grid,.decision-review-grid,.decision-result-grid,.decision-result-links,.tool-fallback-links,.decision-chip-row,.decision-follow-up-grid{grid-template-columns:1fr !important;}.decision-choice,.decision-review-card,.decision-result-card,.decision-result-link,.decision-summary-item,.tool-fallback-link,.decision-chip,.decision-follow-up-link{max-width:100%;width:100%;}.decision-choice strong,.decision-step-name{font-size:14px;}.decision-nav{display:flex;flex-direction:column;position:static;margin-top:18px;padding-top:16px;background:none;}.decision-nav > *{flex:1 1 auto;width:100%;}.decision-nav span{display:none;}.decision-nav .cta,.decision-nav .button-secondary,.decision-email-button{width:100%;min-height:52px;padding:14px 18px;}.decision-result-banner,.decision-result-card,.decision-result-link,.tool-fallback,.decision-loading,.decision-follow-up-card{padding:18px;}.decision-email-capture{grid-template-columns:1fr;}}
@media (max-width:420px){.decision-mobile-calculator-shell{padding:16px;}.decision-kicker,.decision-status{font-size:11px;}.decision-choice,.decision-result-link,.tool-fallback-link,.decision-follow-up-link{padding:14px;}.decision-choice span,.decision-method-note,.decision-trust-note span,.decision-inline-note,.decision-email-note,.decision-follow-up-link span{font-size:13px;}.decision-chip{font-size:13px;}.decision-mobile-calculator-panel,.decision-mobile-calculator-summary,.decision-result-banner,.decision-result-card,.tool-fallback,.decision-loading,.decision-mobile-calculator-step-intro,.decision-step-copy,.decision-question,.decision-trust-note,.decision-follow-up-card{padding:16px;}.decision-mobile-calculator-header h2{font-size:clamp(1.38rem,7.6vw,1.82rem);}}
"""
