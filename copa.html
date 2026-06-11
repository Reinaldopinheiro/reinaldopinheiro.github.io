<?php
// ==========================================
// TODO ESTE BLOCO PHP RODA APENAS NO SERVIDOR
// O USUÁRIO NUNCA CONSEGUIRÁ VER ESTA PARTE!
// ==========================================

$timesPorGrupo = [
    "A" => [ ["n" => "México", "f" => "mx"], ["n" => "África do Sul", "f" => "za"], ["n" => "Coreia do Sul", "f" => "kr"], ["n" => "Tchéquia", "f" => "cz"] ],
    "B" => [ ["n" => "Canadá", "f" => "ca"], ["n" => "Bósnia", "f" => "ba"], ["n" => "Catar", "f" => "qa"], ["n" => "Suíça", "f" => "ch"] ],
    "C" => [ ["n" => "BRASIL", "f" => "br", "b" => true], ["n" => "Marrocos", "f" => "ma"], ["n" => "Haiti", "f" => "ht"], ["n" => "Escócia", "f" => "gb-sct"] ],
    "D" => [ ["n" => "Estados Unidos", "f" => "us"], ["n" => "Paraguai", "f" => "py"], ["n" => "Austrália", "f" => "au"], ["n" => "Turquia", "f" => "tr"] ],
    "E" => [ ["n" => "Alemanha", "f" => "de"], ["n" => "Curaçao", "f" => "cw"], ["n" => "Costa do Marfim", "f" => "ci"], ["n" => "Equador", "f" => "ec"] ],
    "F" => [ ["n" => "Países Baixos", "f" => "nl"], ["n" => "Japão", "f" => "jp"], ["n" => "Suécia", "f" => "se"], ["n" => "Tunísia", "f" => "tn"] ],
    "G" => [ ["n" => "Bélgica", "f" => "be"], ["n" => "Egito", "f" => "eg"], ["n" => "Irã", "f" => "ir"], ["n" => "Nova Zelândia", "f" => "nz"] ],
    "H" => [ ["n" => "Espanha", "f" => "es"], ["n" => "Cabo Verde", "f" => "cv"], ["n" => "Arábia Saudita", "f" => "sa"], ["n" => "Uruguai", "f" => "uy"] ],
    "I" => [ ["n" => "França", "f" => "fr"], ["n" => "Senegal", "f" => "sn"], ["n" => "Iraque", "f" => "iq"], ["n" => "Noruega", "f" => "no"] ],
    "J" => [ ["n" => "Argentina", "f" => "ar"], ["n" => "Argélia", "f" => "dz"], ["n" => "Áustria", "f" => "at"], ["n" => "Jordânia", "f" => "jo"] ],
    "K" => [ ["n" => "Portugal", "f" => "pt"], ["n" => "RD Congo", "f" => "cd"], ["n" => "Uzbequistão", "f" => "uz"], ["n" => "Colômbia", "f" => "co"] ],
    "L" => [ ["n" => "Inglaterra", "f" => "gb-eng"], ["n" => "Croácia", "f" => "hr"], ["n" => "Gana", "f" => "gh"], ["n" => "Panamá", "f" => "pa"] ]
];

function gerarJogosRodada($rodada, $timesPorGrupo) {
    $jogos = [];
    $estadios = ["Dallas", "Los Angeles", "Nova York", "Atlanta", "Miami", "Boston", "Cidade do México", "Toronto", "Vancouver", "Houston", "San Francisco", "Filadélfia"];
    $idxEstadio = 0;
    
    foreach ($timesPorGrupo as $g => $t) {
        $dataDia = 11 + $rodada + floor($idxEstadio / 8);
        $hora = (14 + ($idxEstadio % 3) * 3) . "h";
        
        if ($rodada === 1) {
            $jogos[] = ["data" => $dataDia . "/06", "hora" => $hora, "grupo" => $g, "t1" => $t[0]["n"], "f1" => $t[0]["f"], "t2" => $t[1]["n"], "f2" => $t[1]["f"], "est" => $estadios[$idxEstadio%12], "isBrasil" => isset($t[0]["b"]) || isset($t[1]["b"])]; $idxEstadio++;
            $jogos[] = ["data" => $dataDia . "/06", "hora" => $hora, "grupo" => $g, "t1" => $t[2]["n"], "f1" => $t[2]["f"], "t2" => $t[3]["n"], "f2" => $t[3]["f"], "est" => $estadios[$idxEstadio%12], "isBrasil" => isset($t[2]["b"]) || isset($t[3]["b"])]; $idxEstadio++;
        } elseif ($rodada === 2) {
            $jogos[] = ["data" => ($dataDia+5) . "/06", "hora" => $hora, "grupo" => $g, "t1" => $t[0]["n"], "f1" => $t[0]["f"], "t2" => $t[2]["n"], "f2" => $t[2]["f"], "est" => $estadios[$idxEstadio%12], "isBrasil" => isset($t[0]["b"]) || isset($t[2]["b"])]; $idxEstadio++;
            $jogos[] = ["data" => ($dataDia+5) . "/06", "hora" => $hora, "grupo" => $g, "t1" => $t[1]["n"], "f1" => $t[1]["f"], "t2" => $t[3]["n"], "f2" => $t[3]["f"], "est" => $estadios[$idxEstadio%12], "isBrasil" => isset($t[1]["b"]) || isset($t[3]["b"])]; $idxEstadio++;
        } elseif ($rodada === 3) {
            $jogos[] = ["data" => ($dataDia+10) . "/06", "hora" => "16h", "grupo" => $g, "t1" => $t[3]["n"], "f1" => $t[3]["f"], "t2" => $t[0]["n"], "f2" => $t[0]["f"], "est" => $estadios[$idxEstadio%12], "isBrasil" => isset($t[3]["b"]) || isset($t[0]["b"])]; $idxEstadio++;
            $jogos[] = ["data" => ($dataDia+10) . "/06", "hora" => "16h", "grupo" => $g, "t1" => $t[1]["n"], "f1" => $t[1]["f"], "t2" => $t[2]["n"], "f2" => $t[2]["f"], "est" => $estadios[$idxEstadio%12], "isBrasil" => isset($t[1]["b"]) || isset($t[2]["b"])]; $idxEstadio++;
        }
    }
    return $jogos;
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Central da Copa do Mundo 2026 - RPC Consultoria</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.2.3/css/flag-icons.min.css"/>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
        body { background-color: #f4f6f9; color: #1e293b; padding-bottom: 80px; }
        header {
            background: url('image_0f6aff.png') left center / auto 100% no-repeat, url('image_0f6aff.png') right center / auto 100% no-repeat, linear-gradient(135deg, #1e3a8a 25%, #0d9488 75%);
            color: white; padding: 35px 10px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .header-content-wrapper { max-width: 600px; margin: 0 auto; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6); }
        h1 { font-size: 26px; text-transform: uppercase; font-weight: 800; margin-bottom: 6px; }
        .subtitle { font-size: 14px; opacity: 0.95; }
        .container { max-width: 1200px; margin: 20px auto; padding: 0 15px; }
        .tabs-container { display: flex; background: #cbd5e1; padding: 4px; border-radius: 8px; margin-bottom: 20px; gap: 4px; }
        .tab-btn { flex: 1; padding: 12px; background: none; border: none; font-size: 14px; font-weight: bold; color: #475569; cursor: pointer; border-radius: 6px; text-align: center; }
        .tab-btn.active { background: #1e3a8a; color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .subtabs-container { display: flex; background: #e2e8f0; padding: 4px; border-radius: 6px; margin-bottom: 15px; gap: 4px; overflow-x: auto; }
        .subtab-btn { padding: 8px 16px; background: none; border: none; font-size: 12px; font-weight: bold; color: #475569; cursor: pointer; border-radius: 4px; white-space: nowrap; }
        .subtab-btn.active { background: #0d9488; color: white; }
        .tab-content, .subtab-content { display: none; }
        .tab-content.active, .subtab-content.active { display: block; }
        .status-bar { background-color: #ffffff; border-left: 4px solid #0d9488; padding: 12px; margin-bottom: 20px; font-size: 13px; color: #475569; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
        .groups-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .group-card { background: white; border-radius: 8px; padding: 15px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border-top: 4px solid #0d9488; }
        .group-title { font-size: 15px; font-weight: bold; color: #1e3a8a; margin-bottom: 10px; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }
        .table-wrapper { background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
        table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }
        th { background-color: #1e3a8a; color: white; font-weight: 700; padding: 10px; text-transform: uppercase; }
        td { padding: 10px; border-bottom: 1px solid #e2e8f0; vertical-align: middle; }
        tr:nth-child(even) td { background-color: #f8fafc; }
        .center { text-align: center; } .right { text-align: right; }
        .c-p { font-weight: bold; color: #1e3a8a; }
        tr.brasil-row td { background-color: #f0fdf4 !important; }
        .date-col { font-weight: bold; color: #1e3a8a; }
        .group-badge { background-color: #e2e8f0; color: #334155; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
        tr.brasil-row .group-badge { background-color: #bbf7d0; color: #166534; }
        .flag { display: inline-block; width: 20px; height: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); border-radius: 2px; vertical-align: middle; margin: 0 4px; }
        .brasil-text { font-weight: bold; color: #047857; }
        .placar-wrapper { display: flex; justify-content: center; align-items: center; gap: 6px; }
        .score { background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 4px; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center; font-weight: bold; }
        footer { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #ffffff; border-top: 2px solid #e2e8f0; padding: 15px; text-align: center; font-size: 14px; font-weight: bold; color: #1e3a8a; z-index: 1000; }
    </style>
</head>
<body>

    <header>
        <div class="header-content-wrapper">
            <h1>Central da Copa do Mundo 2026 🏆</h1>
            <div class="subtitle">Tabela Completa de Grupos & Rodadas com o Brasil <span class="fi fi-br" style="width:22px; height:16px;"></span></div>
        </div>
    </header>

    <div class="container">
        <div class="tabs-container">
            <button class="tab-btn active" onclick="switchMainTab('classificacao', event)">📊 Grupos e Classificação</button>
            <button class="tab-btn" onclick="switchMainTab('jogos-grupo', event)">⚽ Fase de Grupos</button>
            <button class="tab-btn" onclick="switchMainTab('mata-mata', event)">🏆 Fases Eliminatórias</button>
        </div>

        <div id="classificacao" class="tab-content active">
            <div class="groups-grid">
                <?php foreach ($timesPorGrupo as $grupo => $selecoes): ?>
                    <div class="group-card">
                        <div class="group-title">Grupo <?php echo $grupo; ?></div>
                        <table>
                            <thead><tr><th>Seleção</th><th class="center">P</th><th class="center">J</th><th class="center">SG</th></tr></thead>
                            <tbody>
                                <?php foreach ($selecoes as $sel): 
                                    $isBr = isset($sel['b']);
                                    $rowClass = $isBr ? "class='brasil-row'" : "";
                                    $txtClass = $isBr ? "class='brasil-text'" : "";
                                ?>
                                    <tr <?php echo $rowClass; ?>>
                                        <td><span class="flag fi fi-<?php echo $sel['f']; ?>"></span> <span <?php echo $txtClass; ?>><?php echo $sel['n']; ?></span></td>
                                        <td class="center c-p">0</td><td class="center">0</td><td class="center">0</td>
                                    </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>

        <div id="jogos-grupo" class="tab-content">
            <div class="subtabs-container">
                <button class="subtab-btn active" onclick="switchSubTab('rodada1', event)">1ª Rodada</button>
                <button class="subtab-btn" onclick="switchSubTab('rodada2', event)">2ª Rodada</button>
                <button class="subtab-btn" onclick="switchSubTab('rodada3', event)">3ª Rodada</button>
            </div>

            <?php for ($r = 1; $r <= 3; $r++): ?>
                <div id="rodada<?php echo $r; ?>" class="subtab-content <?php echo $r===1 ? 'active' : ''; ?>">
                    <div class="table-wrapper">
                        <table>
                            <thead><tr><th class="center">Data/Hora</th><th class="center">Grupo</th><th class="right">Seleção 1</th><th class="center">Placar</th><th>Seleção 2</th><th>Estádio</th></tr></thead>
                            <tbody>
                                <?php 
                                $jogos = gerarJogosRodada($r, $timesPorGrupo);
                                foreach ($jogos as $j): 
                                    $rowClass = $j['isBrasil'] ? "class='brasil-row'" : "";
                                    $t1Class = $j['t1'] === "BRASIL" ? "class='brasil-text'" : "";
                                    $t2Class = $j['t2'] === "BRASIL" ? "class='brasil-text'" : "";
                                ?>
                                    <tr <?php echo $rowClass; ?>>
                                        <td class="center date-col"><?php echo $j['data']; ?><br><span style="font-size:11px; font-weight:normal; color:#64748b;"><?php echo $j['hora']; ?></span></td>
                                        <td class="center"><span class="group-badge"><?php echo $j['grupo']; ?></span></td>
                                        <td class="right"><span <?php echo $t1Class; ?>><?php echo $j['t1']; ?></span> <span class="flag fi fi-<?php echo $j['f1']; ?>"></span></td>
                                        <td class="center"><div class="placar-wrapper"><div class="score"></div><span style="color:#94a3b8;">x</span><div class="score"></div></div></td>
                                        <td><span class="flag fi fi-<?php echo $j['f2']; ?>"></span> <span <?php echo $t2Class; ?>><?php echo $j['t2']; ?></span></td>
                                        <td style="color:#64748b; font-size:12px;"><?php echo $j['est']; ?></td>
                                    </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>
            <?php endfor; ?>
        </div>

        <div id="mata-mata" class="tab-content">
            <div class="subtabs-container">
                <button class="subtab-btn active" onclick="switchSubTab('fase-32', event)">Dezesseis-avos</button>
                <button class="subtab-btn" onclick="switchSubTab('fase-final', event)">Final 🏆</button>
            </div>
            <div id="fase-32" class="subtab-content active">
                <div class="table-wrapper">
                    <table>
                        <tbody>
                            <?php for($i=1; $i<=16; $i++): ?>
                                <tr>
                                    <td class="center" style="font-weight:bold; color:#0d9488;">Dezesseis-avos [J<?php echo $i; ?>]</td>
                                    <td class="center">A definir</td>
                                    <td class="right">Classificado <?php echo (2*$i-1); ?></td>
                                    <td class="center"><div class="placar-wrapper"><div class="score"></div> x <div class="score"></div></div></td>
                                    <td>Classificado <?php echo (2*$i); ?></td>
                                    <td>Arena FIFA</td>
                                </tr>
                            <?php endfor; ?>
                        </tbody>
                    </table>
                </div>
            </div>
            <div id="fase-final" class="subtab-content">
                <div class="table-wrapper">
                    <table>
                        <tbody>
                            <tr>
                                <td class="center" style="font-weight:bold; color:#1e3a8a; background-color:#e0f2fe;">Grande Final 🏆</td>
                                <td class="center" style="background-color:#e0f2fe; font-weight:bold;">19/07 - 17h</td>
                                <td class="right" style="background-color:#e0f2fe; font-weight:bold;"><span class="brasil-text">BRASIL</span> <span class="flag fi fi-br"></span></td>
                                <td class="center" style="background-color:#e0f2fe;"><div class="placar-wrapper"><div class="score" style="border-color:#1e3a8a;"></div> x <div class="score" style="border-color:#1e3a8a;"></div></div></td>
                                <td style="background-color:#e0f2fe; font-weight:bold;">Vencedor Semifinal 2</td>
                                <td style="background-color:#e0f2fe; font-weight:bold;">Nova York / NJ</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <footer>Oferecimento: RPC - Reinaldo Pinheiro Consultoria</footer>

    <script>
        function switchMainTab(tabId, event) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
            const primeiraSubAba = document.getElementById(tabId).querySelector('.subtab-btn');
            if (primeiraSubAba) { primeiraSubAba.click(); }
        }
        function switchSubTab(subTabId, event) {
            const pai = document.getElementById(subTabId).parentElement;
            pai.querySelectorAll('.subtab-content').forEach(el => el.classList.remove('active'));
            pai.querySelectorAll('.subtab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(subTabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }
        
        // Bloqueios adicionais preventivos para usuários leigos
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('keydown', e => {
            if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && ['I','J'].includes(e.key.toUpperCase())) || (e.ctrlKey && e.key.toUpperCase() === 'U')) {
                e.preventDefault();
            }
        });
    </script>
</body>
</html>