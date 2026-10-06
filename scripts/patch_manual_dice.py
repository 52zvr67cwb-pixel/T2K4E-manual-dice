from pathlib import Path

app = Path('src/App.jsx')
text = app.read_text(encoding='utf-8')

old = '''const d6 = () => Math.floor(Math.random() * 6) + 1;
const d8 = () => Math.floor(Math.random() * 8) + 1;
const twoD3 = () => {
    const r1 = Math.floor(Math.random() * 3) + 1;
    const r2 = Math.floor(Math.random() * 3) + 1;
    return { rolls: [r1, r2], total: r1 + r2 };
};
const rollCheck = (attrDie, skillDie) => {
    if (!attrDie) return { success: false, attrDie: 'None', skillDie: skillDie || 'None', attrRoll: 0, skillRoll: 0 };
    const attrRoll = Math.floor(Math.random() * gameData.DIE_SIZES[attrDie]) + 1;
    const skillRoll = skillDie ? Math.floor(Math.random() * gameData.DIE_SIZES[skillDie]) + 1 : 0;
    return {
        success: attrRoll >= 6 || skillRoll >= 6,
        attrDie,
        skillDie: skillDie || 'None',
        attrRoll,
        skillRoll
    };
};'''

new = '''// ===================================================================================
// --- PHYSICAL DICE MODE ---
// Every actual lifepath die roll is supplied by the player. The surrounding creator
// remains unchanged: the entered result is returned wherever the original creator
// would have generated a random die result.
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
};'''

if old not in text:
    raise SystemExit('Expected original dice helper block was not found; refusing to modify the app.')

text = text.replace(old, new, 1)
text = text.replace('const warRoll = d8();', "const warRoll = d8('War Check');")
text = text.replace('const prisonRoll = d6();', "const prisonRoll = d6('Prison Check');")
text = text.replace('const ageIncrease = d6();', "const ageIncrease = d6('Age Increase');")
text = text.replace('const agingRoll = d8();', "const agingRoll = d8('Aging Check');")
text = text.replace('const listRoll = d6();', "const listRoll = d6('Officer Specialty Table');")
text = text.replace('const specialtyRoll = d6();', "const specialtyRoll = d6('Specialty Roll');")
text = text.replace('const rads = d6();', "const rads = d6('Permanent Radiation');")

app.write_text(text, encoding='utf-8')
print('Patched physical-dice mode successfully.')
