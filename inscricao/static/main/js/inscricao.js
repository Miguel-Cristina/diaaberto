function CheckEscola(val) {
    let element = document.getElementById('form_escola');
    if (val === 'others') {
        element.style.display = 'block';
        document.getElementById("id_nome").setAttribute("required", "required")
        document.getElementById("id_morada").setAttribute("required", "required")
        document.getElementById("id_codigo_postal").setAttribute("required", "required")
        document.getElementById("id_contacto").setAttribute("required", "required")
        document.getElementById("id_localidade").setAttribute("required", "required")
    } else {
        element.style.display = 'none';
        document.getElementById("id_nome").removeAttribute("required");
        document.getElementById("id_morada").removeAttribute("required");
        document.getElementById("id_codigo_postal").removeAttribute("required");
        document.getElementById("id_contacto").removeAttribute("required");
        document.getElementById("id_localidade").removeAttribute("required");
    }
}

function tipoTransporte(val) {
    let transporte_para_campus = document.getElementById('transporte_para_campus')
    if (val === 'proprio') {
        transporte_para_campus.style.display = 'none';
        document.getElementById('id_QuerTransportePara_0').removeAttribute("required");
        document.getElementById('id_QuerTransportePara_1').removeAttribute("required");
    } else {
        transporte_para_campus.style.display = 'block';
        document.getElementById('id_QuerTransportePara_0').setAttribute("required", "required");
        document.getElementById('id_QuerTransportePara_1').removeAttribute("required");
    }
}

function paraCampus(val) {
    let qual_campus = document.getElementById('qual_campus')
    let qual_campus2 = document.getElementById('id_QuerTransportePara')
    let qual_campus3 = document.getElementById('qual_campus_2')
    if (val === 'nao') {
        qual_campus.style.display = 'none';
        qual_campus2.removeAttribute("required");
        qual_campus3.removeAttribute("required");
    } else {
        qual_campus.style.display = 'block';
        qual_campus2.setAttribute("required", "required");
        qual_campus3.setAttribute("required", "required");
    }
}

function entreCampus(val) {
    let relogio3 = document.getElementById('entre_campus')
    let DivRelogio3 = document.getElementById('timepicker-three_div')
    let DivRelogio4 = document.getElementById('timepicker-four_div')
    if (val === 'nao') {
        relogio3.style.display = 'none'
        DivRelogio3.style.display = 'none'
        DivRelogio4.style.display = 'none'
    } else if (val === 'ida') {
        relogio3.style.display = 'block'
        DivRelogio3.style.display = 'block'
        DivRelogio4.style.display = 'none'
    } else if (val === 'idavolta') {
        relogio3.style.display = 'block'
        DivRelogio3.style.display = 'block'
        DivRelogio4.style.display = 'block'
    }
}

function entreCampusRelogio(val) {
    let DivRelogio3 = document.getElementById('timepicker-three_div')
    let DivRelogio4 = document.getElementById('timepicker-four_div')
    if (val === 'penha_para_gambelas' || val === 'gambelas_para_penha') {
        if (val === 'penha_para_gambelas') {
            document.getElementById('timepicker-three_label').textContent = "Horario ida da Penha para Gambelas"
            document.getElementById('timepicker-four_label').textContent = "Horario volta das Gambelas para a Penha"
        } else if (val === 'gambelas_para_penha') {
            document.getElementById('timepicker-three_label').textContent = "Horario ida das Gambelas para a Penha"
            document.getElementById('timepicker-four_label').textContent = "Horario volta da Penha para Gambelas"
        }
    } else
        DivRelogio3.style.display = 'none'
}

function CheckRefeicao(val) {
    let refeicao = document.getElementById('quer_refeicao');
    if (val === "sim") {
        refeicao.style.display = 'block';
    } else if (val === 'nao') {
        refeicao.style.display = 'none';
        document.getElementById("id_numero_aluno_normal").value = '0';
        document.getElementById("id_numero_outro_normal").value = '0';
        MultiplicaPreco();
    }
}

function MultiplicaPreco() {
    let num1 = document.getElementById("id_numero_aluno_normal").value;
    let num2 = document.getElementById("id_numero_outro_normal").value;
    let preco1 = parseFloat(document.getElementById("preco_aluno_normal").value);
    let preco2 = parseFloat(document.getElementById("preco_outro_normal").value);
    let final = (num1 * preco1) + (num2 * preco2);
    document.getElementById("preco_total").setAttribute("value", final.toFixed(2).toString());
}

let max_incritos = 0;
let atividades = [];
let inscritos = [];
let sessao = [];


let row_count = 0
let row_deleted_incremental = 0
let deleted_rows = 0

function EscolherSessao(atividade_id, sessao_id, ini, dur,
                        nome, loc, cam, vag, ses_id) {
    let val = document.getElementById('quantity_' + sessao_id).value;
    let table_inscrito = document.getElementById("inscritos_body");
    let table_inscrito_length = document.getElementById("inscritos_body").rows.length;
    let row_id = 0;
    let i;
    for (i = 0; i < table_inscrito_length; i++) {
        if (table_inscrito.rows[i].id === sessao_id)
            row_id = table_inscrito.rows[i].id
    }
    let ses_id_plica = "'" + ses_id + "'"
    let sessao_id_plica = "'" + sessao_id + "'"
    if (row_id !== 0) {
        row_count--
        let row = document.getElementById(sessao_id).cells;
        row[2].innerHTML = '<div class="field has-numberinput has-numberinput-compact">\n' +
            '<div class="b-numberinput field has-addons" style="width: 7rem;">\n' +
            '<p class="control">\n' +
            '<button type="button" class="button is-primary" onclick="incremental(\'minus\', \'quantity_' + sessao_id + '\'); EscolherSessao( \'' + atividade_id + '\', \'' + sessao_id + '\',\n' +
            '                                                                                                                                                               \'' + ini + '\', \'' + dur + '\',\n' +
            '                                                                                                                                                               \'' + nome + '\', \'' + loc + '\',\n' +
            '                                                                                                                                                               \'' + cam + '\', \'' + vag + '\',\'' + ses_id + '\')">' +
            '<span class="icon">\n' +
            '<i class="mdi mdi-minus mdi-24px"></i>\n' +
            '</span>\n' +
            '</button>\n' +
            '</p>' +
            '<div class="control is-clearfix">' +
            '<input type="number" class="input" id="inscritos_sessao_' + sessao_id +
            '"  name="inscritos_sessao_' + row_count + '" value="' + val +
            '" min="0" max="' + vag +
            '" onchange="AlterarInscritos(' + ses_id_plica + ', this.value, ' + sessao_id_plica + ')">' +
            '</div>\n' +
            '<p class="control">\n' +
            '<button type="button" class="button is-primary" onclick="incremental(\'add\', \'quantity_' + sessao_id + '\'); EscolherSessao( \'' + atividade_id + '\', \'' + sessao_id + '\',\n' +
            '                                                                                                                                                               \'' + ini + '\', \'' + dur + '\',\n' +
            '                                                                                                                                                               \'' + nome + '\', \'' + loc + '\',\n' +
            '                                                                                                                                                               \'' + cam + '\', \'' + vag + '\',\'' + ses_id + '\')">' +
            '<span class="icon">\n' +
            '<i class="mdi mdi-plus mdi-24px"></i>\n' +
            '</span>\n' +
            '</button>\n' +
            '</p>\n' +
            '</div>\n';
        row_count++
    } else if (val !== "0") {
        let row = table_inscrito.insertRow(-1)
        row.id = sessao_id
        row.name = "row_" + row_count
        row.draggable = "false"
        let inicio = row.insertCell(0)
        let duracao = row.insertCell(1)
        let inscritos = row.insertCell(2)
        let atividade = row.insertCell(3)
        let local = row.insertCell(4)
        let campus = row.insertCell(5)
        let acao = row.insertCell(6)
        inicio.innerHTML = ini
        duracao.innerHTML = dur + " min"
        inscritos.innerHTML = '<div class="field has-numberinput has-numberinput-compact">\n' +
            '<div class="b-numberinput field has-addons" style="width: 7rem;">\n' +
            '<p class="control">\n' +
            '<button type="button" class="button is-primary" onclick="incremental(\'minus\', \'quantity_' + sessao_id + '\'); EscolherSessao( \'' + atividade_id + '\', \'' + sessao_id + '\',\n' +
            '                                                                                                                                                               \'' + ini + '\', \'' + dur + '\',\n' +
            '                                                                                                                                                               \'' + nome + '\', \'' + loc + '\',\n' +
            '                                                                                                                                                               \'' + cam + '\', \'' + vag + '\',\'' + ses_id + '\')">' +
            '<span class="icon">\n' +
            '<i class="mdi mdi-minus mdi-24px"></i>\n' +
            '</span>\n' +
            '</button>\n' +
            '</p>' +
            '<div class="control is-clearfix">' +
            '<input type="number" class="input" id="inscritos_sessao_' + sessao_id +
            '"  name="inscritos_sessao_' + row_count + '" value="' + val +
            '" min="0" max="' + vag +
            '" onchange="AlterarInscritos(' + ses_id_plica + ', this.value, ' + sessao_id_plica + ')">' +
            '</div>\n' +
            '<p class="control">\n' +
            '<button type="button" class="button is-primary" onclick="incremental(\'add\', \'quantity_' + sessao_id + '\'); EscolherSessao( \'' + atividade_id + '\', \'' + sessao_id + '\',\n' +
            '                                                                                                                                                               \'' + ini + '\', \'' + dur + '\',\n' +
            '                                                                                                                                                               \'' + nome + '\', \'' + loc + '\',\n' +
            '                                                                                                                                                               \'' + cam + '\', \'' + vag + '\',\'' + ses_id + '\')">' +
            '<span class="icon">\n' +
            '<i class="mdi mdi-plus mdi-24px"></i>\n' +
            '</span>\n' +
            '</button>\n' +
            '</p>\n' +
            '</div>\n';
        atividade.innerHTML = nome + '<input type="number" id="sessao_atividade_' + sessao_id +
            '" name="sessao_atividade_' + row_count + '" value="' + sessao_id + '" hidden>' +
            '<input type="number" id="deleted_ref_' + sessao_id + '" value="' + row_count + '" hidden>'
        local.innerHTML = loc.toString()
        campus.innerHTML = cam.toString()
        let inscritos_value = "'0'"
        acao.className = 'has-text-centered'
        acao.innerHTML = '<p onclick="AlterarInscritos(' + ses_id_plica + ', ' + inscritos_value +
            ', ' + sessao_id_plica + ')"><a>\n' +
            '<span class="icon has-text-danger"><i class="mdi mdi-close-box mdi-24px"></i></span></a></p>'
        row_count++
        makecount()
    }
    if (document.getElementById("inscritos_sessao_" + sessao_id).value === "0")
        deleteSessao(sessao_id)
    contarSessoesInscritas()
}

function AlterarInscritos(ses_id, val, row_id) {
    document.getElementById(ses_id).value = val
    if (val === "0")
        deleteSessao(row_id)
    contarSessoesInscritas()
}

function deleteSessao(row_id) {
    let x = document.getElementById('deleted_ref_' + row_id).value
    let table_deleted = document.getElementById("rows_deleted_table");
    let row_deleted = table_deleted.insertRow(-1)
    let cell = row_deleted.insertCell(0)
    cell.innerHTML = '<input type="number" id="row_deleted_' + row_deleted_incremental.toString() +
        '" name="row_deleted_' + row_deleted_incremental.toString() + '" value="' + x.toString() + '" hidden>'
    row_deleted_incremental++
    let row = document.getElementById(row_id)
    row.parentElement.removeChild(row)
    deleted_rows++
    makecount()
}

function makecount() {
    document.getElementById("row_countt").setAttribute("value", row_count.toString());
    document.getElementById("row_deletedd").setAttribute("value", deleted_rows.toString())
}

function contarSessoesInscritas() {
    let inscritos_length = document.getElementById("inscritos_body").rows.length;
    if (inscritos_length === 0) {
        document.getElementById("sem_inscritos").style.display = 'block'
        document.getElementById("inscritos_body").style.display = 'none'
        document.getElementById("inscritos_head").style.display = 'none'
    } else if (inscritos_length > 0) {
        document.getElementById("sem_inscritos").style.display = 'none'
        document.getElementById("inscritos_body").style.display = ''
        document.getElementById("inscritos_head").style.display = ''
    }
}


function expandAtividade(id) {
    let icon = document.getElementById('icon_' + id)
    if (icon.classList.contains('is-expanded')) {
        icon.classList.remove('is-expanded')
    } else {
        icon.classList.add('is-expanded')
    }
}

let pag = "1"

function pagination(id) {
    if (id === "next") {
        let next = (parseInt(pag) + 1).toString()
        document.getElementById('pag' + pag).style.display = 'none'
        document.getElementById('pag' + next).style.display = ''
        document.getElementById('bar' + pag).classList.remove('is-active')
        document.getElementById('bar' + pag).classList.add('is-previous')
        document.getElementById('bar' + next).classList.add('is-active')
        pag = next
    } else if (id === "back1") {
        let back = (parseInt(pag) - 1).toString()
        document.getElementById('pag' + pag).style.display = 'none'
        document.getElementById('pag' + back).style.display = ''
        document.getElementById('bar' + pag).classList.remove('is-active')
        document.getElementById('bar' + back).classList.remove('is-previous')
        document.getElementById('bar' + back).classList.add('is-active')
        pag = back
    } else if (id === 'confirmacao') {
        document.getElementById('popup_confirmacao').style.display = ''
    } else if (id === 'popup_cancel') {
        document.getElementById('popup_confirmacao').style.display = 'none'
    }
    if (pag !== "1") {
        document.getElementById('cancel').style.display = 'none'
        document.getElementById('back1').style.display = ''
    } else if (pag === "1") {
        document.getElementById('cancel').style.display = ''
        document.getElementById('back1').style.display = 'none'
    }
    if (pag === "5") {
        document.getElementById('next').style.display = 'none'
        document.getElementById('confirmacao').style.display = ''
    } else if (pag !== "5") {
        document.getElementById('next').style.display = ''
        document.getElementById('confirmacao').style.display = 'none'
    }
}

function incremental(type, id) {
    let value = document.getElementById(id).getAttribute('value')
    if (type === 'add') {
        document.getElementById(id).stepUp(1)
    } else if (type === 'minus') {
        document.getElementById(id).stepDown(1)
    }
    document.getElementById(id).setAttribute('value', value)
}

