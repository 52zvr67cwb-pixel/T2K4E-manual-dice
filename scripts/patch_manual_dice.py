from pathlib import Path

app = Path('src/App.jsx')
text = app.read_text(encoding='utf-8')

start = text.find('const d6 = () =>')
end = text.find('const getDie =', start)
if start < 0 or end < 0:
    raise SystemExit('Could not locate the creator dice helper section; refusing to modify the app.')

new = '''// ===================================================================================
// --- PHYSICAL DICE MODE ---
// ===================================================================================
const manualDie = (sides, context) => {
    while (true) {
        const input = window.prompt(
            `🎲 PHYSICAL DICE REQUIRED\\n\\nRoll a d${sides} for:\\n${context}\\n\\nEnter your result (1-${sides}):`
        );
        if (input !== null && /^\\d+$/.test(input.trim())) {
            const result = Number(input.trim());
            if (result >= 1 && result <= sides) return result;
        }
        window.alert(`Please enter a whole-number result from 1 to ${sides}.`);
    }
};

const d6 = (context = 'D6 roll') => manualDie(6, context);
const d8 = (context = 'D8 roll') => manualDie(8, context);
const twoD3 = () => {
    const r1 = manualDie(3, 'Initial Attribute Increase — Die 1');
    const r2 = manualDie(3, 'Initial Attribute Increase — Die 2');
    return { rolls: [r1, r2], total: r1 + r2 };
};
const rollCheck = (attrDie, skillDie) => {
    if (!attrDie) return { success: false, attrDie: 'None', skillDie: skillDie || 'None', attrRoll: 0, skillRoll: 0 };
    const attrRoll = manualDie(gameData.DIE_SIZES[attrDie], `Promotion Check — ${attrDie}`);
    const skillRoll = skillDie ? manualDie(gameData.DIE_SIZES[skillDie], `Promotion Check — ${skillDie}`) : 0;
    return {
        success: attrRoll >= 6 || skillRoll >= 6,
        attrDie,
        skillDie: skillDie || 'None',
        attrRoll,
        skillRoll
    };
};
'''

text = text[:start] + new + text[end:]

vite = Path('vite.config.js')
if vite.exists():
    vite_text = vite.read_text(encoding='utf-8')
    vite_text = vite_text.replace("base: '/t2k4e-creator/'", "base: '/T2K4E-manual-dice/'")
    vite.write_text(vite_text, encoding='utf-8')

app.write_text(text, encoding='utf-8')
print('Patched physical dice mode successfully.')
