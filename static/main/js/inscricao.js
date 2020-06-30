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
    if (val === 'Transporte próprio') {
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
            '" style="cursor: text" readonly onchange="AlterarInscritos(' + ses_id_plica + ', this.value, ' + sessao_id_plica + ')">' +
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
            '" style="cursor: text" readonly onchange="AlterarInscritos(' + ses_id_plica + ', this.value, ' + sessao_id_plica + ')">' +
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
        acao.innerHTML = '<p class="button has-text-white is-small" onclick="AlterarInscritos(' + ses_id_plica + ', ' + inscritos_value +
            ', ' + sessao_id_plica + ')"><a>\n' +
            '<span class="icon is-small has-text-danger">\n' +
            '                <i class="has-text-red mdi-close-box mdi-36px mdi mdi-chevron-right mdi-24px"></i>\n' +
            '            </span></a></p>'
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

function pagination(id, participante, age) {
    if (id === "next") {
        let errormsg1 = '<div id="message_container" class="notices is-bottom">\n' +
            '    <div role="alert" class="toast is-danger is-bottom" style="">\n' +
            '        <div id="msg_here">'
        let errormsg2 = '</div>\n' +
            '    </div>\n' +
            '</div>'
        let msgdiv = document.getElementById('msgdiv')

        let dia
        let area
        let ano
        let p
        let alunos
        let professores
        let file
        let nome
        let morada
        let codigo_postal
        let localidade
        let contacto
        let escola
        let todasescolas = ""
        let radio_refeicao
        let refAlunos;
        let refOutros;
        let tipoTransporte;
        let transporteEstacao;
        let horaChegada;
        let qualcampus;
        let qualcampus2;
        let horaIda;
        let horaVolta;
        let horaPartida
        let transporteEntreValue
        if (pag === '1') {
            dia = document.forms["inscricao_form"]["data_inscricao"].value;
            area = document.forms["inscricao_form"]["area_estudos"].value;
            ano = document.forms["inscricao_form"]["ano_estudos"].value;
            if (participante === 'Participante Individual') {
                p = document.forms["inscricao_form"]["acompanhantes"].value;
                if (age < 18)
                    file = document.forms["inscricao_form"]["myfile"].value;
            } else if (participante === 'Participante em Grupo') {
                p = document.forms["inscricao_form"]["turma"].value;
                alunos = document.forms["inscricao_form"]["total_participantes"].value;
                professores = document.forms["inscricao_form"]["total_professores"].value;
            }
        } else if (pag === '2') {
            escola = document.forms["inscricao_form"]["Escola"].value;
            if (escola === "others") {
                nome = document.forms["inscricao_form"]["nome"].value.toLowerCase();
                nome = nome.normalize('NFD').replace(/[\u0300-\u036f]/g, "")
                morada = document.forms["inscricao_form"]["morada"].value;
                codigo_postal = document.forms["inscricao_form"]["codigo_postal"].value;
                localidade = document.forms["inscricao_form"]["localidade"].value;
                contacto = document.forms["inscricao_form"]["contacto"].value;
            }
            let x = document.getElementById("Escola");
            let i;
            for (i = 0; i < x.length; i++) {
                todasescolas = todasescolas + "\n" + x.options[i].text;
            }
            todasescolas = todasescolas.normalize('NFD').replace(/[\u0300-\u036f]/g, "")
        } else if (pag === '3') {
            radio_refeicao = document.forms["inscricao_form"]["QuerRefeicao"].value;
            if (radio_refeicao === '') {
                radio_refeicao = "null"
            } else if (radio_refeicao === "sim") {
                refAlunos = document.forms["inscricao_form"]["numero_aluno_normal"].value;
                refOutros = document.forms["inscricao_form"]["numero_outro_normal"].value;
            }
        } else if (pag === '4') {
            tipoTransporte = document.forms["inscricao_form"]["tipo_transporte"].value;
            if (tipoTransporte === "Autocarro Publico" || tipoTransporte === "Comboio") {
                transporteEstacao = document.forms["inscricao_form"]["QuerTransportePara"].value;
                if (transporteEstacao === "sim") {
                    qualcampus = document.forms["inscricao_form"]["qual"].value;
                }
            }
            horaChegada = document.forms["inscricao_form"]["timepicker-one"].value;
            horaPartida = document.forms["inscricao_form"]["timepicker-two"].value;
            transporteEntreValue = document.forms["inscricao_form"]["QuerTransporteEntre"].value;
            if (transporteEntreValue === "ida" || transporteEntreValue === "idavolta") {
                qualcampus2 = document.forms["inscricao_form"]["transporte_campus"].value;
                if (qualcampus2 !== "escolher") {
                    horaIda = document.forms["inscricao_form"]["timepicker-three"].value;
                    if (transporteEntreValue === "idavolta") {
                        horaVolta = document.forms["inscricao_form"]["timepicker-four"].value;
                    }
                }
            }
        }
        if (pag === '1' && dia === "") {
            msgdiv.innerHTML = errormsg1 + 'Deve escolher o dia que pretende participar' + errormsg2
        } else if (pag === '1' && area === "escolha") {
            msgdiv.innerHTML = errormsg1 + 'Deve de escolher a área de estudos' + errormsg2
        } else if (pag === '1' && (ano < 0 || ano > 12 || ano === '')) {
            msgdiv.innerHTML = errormsg1 + 'Deve de indicar o ano de estudos' + errormsg2
        } else if (pag === '1' && participante === 'Participante em Grupo' && !RegExp("^[A-zÀ-ÿ0-9ºª ]+$").test(p)) {
            msgdiv.innerHTML = errormsg1 + 'Deve de indicar a turma' + errormsg2
        } else if (pag === '1' && participante === 'Participante em Grupo' && alunos <= 0) {
            msgdiv.innerHTML = errormsg1 + 'Deve de indicar o numero total alunos' + errormsg2
        } else if (pag === '1' && participante === 'Participante em Grupo' && professores <= 0) {
            msgdiv.innerHTML = errormsg1 + 'Deve de indicar o número total professores' + errormsg2
        } else if (pag === '1' && participante === 'Participante Individual' && (p < 0 || p === '')) {
            msgdiv.innerHTML = errormsg1 + 'Deve de indicar o número acompanhantes' + errormsg2
        } else if (pag === '1' && participante === 'Participante Individual' && age < 18 && !(RegExp("[a-zA-Z0-9-_]+.pdf$").test(file) || RegExp("[a-zA-Z0-9-_]+.png$").test(file) || RegExp("[a-zA-Z0-9-_]+.PNG$").test(file))) {
            msgdiv.innerHTML = errormsg1 + 'Deve de fazer updload do PDF ou PNG de autorização' + errormsg2
        } else if (pag === '2' && escola === "Escolher") {
            msgdiv.innerHTML = errormsg1 + 'Deve de escolher uma escola adequada' + errormsg2
        } else if (pag === '2' && escola === "others" && !RegExp('^[A-zÀ-ÿ0-9ºª ]+$').test(nome)) {
            msgdiv.innerHTML = errormsg1 + 'Deve de escolher um nome de escola adequada' + errormsg2
        } else if (pag === '2' && escola === "others" && RegExp('^[ ]+$').test(nome)) {
            msgdiv.innerHTML = errormsg1 + 'Deve de escolher um nome de escola adequada' + errormsg2
        } else if (pag === '2' && escola === "others" && todasescolas.toLowerCase().includes(nome)) {
            msgdiv.innerHTML = errormsg1 + 'Escola criada já existe' + errormsg2
        } else if (pag === '2' && escola === "others" && !RegExp('^[A-zÀ-ÿ0-9ºª ]+$').test(morada)) {
            msgdiv.innerHTML = errormsg1 + 'Deve de escolher uma morada da escola' + errormsg2
        } else if (pag === '2' && escola === "others" && RegExp('^[ ]+$').test(morada)) {
            msgdiv.innerHTML = errormsg1 + 'Deve de escolher uma morada da escola' + errormsg2
        } else if (pag === '2' && escola === "others" && !RegExp('^[0-9]{4}-[0-9]{3}$').test(codigo_postal)) {
            msgdiv.innerHTML = errormsg1 + 'Deve de usar um código postal valido da escola' + errormsg2
        } else if (pag === '2' && escola === "others" && !RegExp('^[A-zÀ-ÿ0-9 ]+$').test(localidade)) {
            msgdiv.innerHTML = errormsg1 + 'Deve de usar uma localidade válida da escola' + errormsg2
        } else if (pag === '2' && escola === "others" && RegExp('^[ ]+$').test(localidade)) {
            msgdiv.innerHTML = errormsg1 + 'Deve de usar uma localidade valida da escola' + errormsg2
        } else if (pag === '2' && escola === "others" && !RegExp('^[0-9]{9}$').test(contacto)) {
            msgdiv.innerHTML = errormsg1 + 'Deve de usar um contacto valido da escola' + errormsg2
        } else if (pag === '3' && radio_refeicao === "null") {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar se requer refeição' + errormsg2
        } else if (pag === '3' && radio_refeicao === "sim" && (refAlunos <= 0 || refOutros <= 0)) {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar o número de refeições correto' + errormsg2
        } else if (pag === '4' && tipoTransporte === "escolher") {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar o tipo transporte que irá usar' + errormsg2
        } else if (pag === '4' && (tipoTransporte === "Autocarro Publico" || tipoTransporte === "Comboio") && transporteEstacao === "sim" && qualcampus === "escolher") {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar para que campos necessita de transporte desde a estação' + errormsg2
        } else if (pag === '4' && horaChegada === horaPartida) {
            msgdiv.innerHTML = errormsg1 + 'Hora de chegada e de partida não podem coincidir' + errormsg2
        } else if (pag === '4' && horaChegada >= horaPartida) {
            msgdiv.innerHTML = errormsg1 + 'Hora de chegada e de partida incoerentes' + errormsg2
        } else if (pag === '4' && horaChegada === "00 : 00") {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de chegada correta' + errormsg2
        } else if (pag === '4' && horaPartida === "00 : 00") {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de partida correta' + errormsg2
        } else if (pag === '4' && transporteEntreValue !== "nao" && qualcampus2 === "escolher") {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar de qual para qual campus necessita de transporte' + errormsg2
        } else if (pag === '4' && transporteEntreValue === "ida" && qualcampus2 !== "escolher" && horaIda === "00 : 00") {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de ida correta' + errormsg2
        } else if (pag === '4' && transporteEntreValue === "idavolta" && qualcampus2 !== "escolher" && horaIda === horaVolta) {
            msgdiv.innerHTML = errormsg1 + 'Hora de ida e de volta não podem coincidir' + errormsg2
        } else if (pag === '4' && transporteEntreValue === "idavolta" && qualcampus2 !== "escolher" && horaIda >= horaVolta) {
            msgdiv.innerHTML = errormsg1 + 'Hora de ida e de volta incoerentes' + errormsg2
        } else if (pag === '4' && transporteEntreValue === "idavolta" && qualcampus2 !== "escolher" && horaIda === "00 : 00") {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de ida correta' + errormsg2
        } else if (pag === '4' && transporteEntreValue === "idavolta" && qualcampus2 !== "escolher" && horaVolta === "00 : 00") {
            msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de ida correta' + errormsg2
        } else {
            let next = (parseInt(pag) + 1).toString()
            document.getElementById('pag' + pag).style.display = 'none'
            document.getElementById('pag' + next).style.display = ''
            document.getElementById('bar' + pag).classList.remove('is-active')
            document.getElementById('bar' + pag).classList.add('is-previous')
            document.getElementById('bar' + next).classList.add('is-active')
            pag = next
        }
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

    var message_ele = document.getElementById("message_container");
    setTimeout(function () {
        message_ele.style.display = "none";
    }, 4000);
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


function incremental_max_estudantes(type, id, tipo) {
    let value = document.getElementById(id).getAttribute('value')
    let x
    if (type === 'add') {
        x = document.getElementById(id)
        x.stepUp(1)
    } else if (type === 'minus') {
        x = document.getElementById(id)
        x.stepDown(1)
    }
    if (tipo === "Participante em Grupo") {
        document.getElementById('id_numero_aluno_normal').setAttribute('max', x.value)
    } else if (tipo === "Participante Individual") {
        document.getElementById('id_numero_aluno_normal').setAttribute('max', '1')
    }
    document.getElementById(id).setAttribute('value', value)
}


function incremental_max_outros(type, id) {
    let value = document.getElementById(id).getAttribute('value')
    let x
    if (type === 'add') {
        x = document.getElementById(id)
        x.stepUp(1)
    } else if (type === 'minus') {
        x = document.getElementById(id)
        x.stepDown(1)
    }
    document.getElementById('id_numero_outro_normal').setAttribute('max', x.value)
    document.getElementById(id).setAttribute('value', value)
}


function incremental_atividades(type, id, dia, tipo) {
    let value = document.getElementById(id).getAttribute('value')
    let dia_inscricao = document.getElementById('data_inscricao').value
    let dia_value = document.getElementById(dia).value
    console.log("dia_inscricao: " + dia_inscricao)
    console.log("dia_id: " + dia)
    console.log("dia_value: " + dia_value)
    let errormsg1 = '<div id="message_container" class="notices is-bottom">\n' +
        '    <div role="alert" class="toast is-danger is-bottom" style="">\n' +
        '        <div id="msg_here">'
    let errormsg2 = '</div>\n' +
        '    </div>\n' +
        '</div>'

    if (tipo === "Participante em Grupo") {
        let maxGrupo = document.getElementById('id_total_participantes').value
        document.getElementById(id).setAttribute('max', maxGrupo)

        console.log(maxGrupo)
    }
    if (type === 'add') {
        if (dia_value === dia_inscricao) {
            document.getElementById(id).stepUp(1)
            document.getElementById(id).setAttribute('value', value)
            console.log("dia_value === dia_inscricao")
        } else if (dia_inscricao === "") {
            document.getElementById('msgdiv').innerHTML = errormsg1 + 'Deve escolher o dia em que vai participar no dia aberto' + errormsg2
            console.log("dia_inscricao===null")
        } else {
            console.log("else")
            document.getElementById('msgdiv').innerHTML = errormsg1 + 'Deve escolher uma sessão do mesmo dia que vai participar no dia aberto' + errormsg2
        }
    } else if (type === 'minus') {
        document.getElementById(id).stepDown(1)
        document.getElementById(id).setAttribute('value', value)
    }
    var message_ele = document.getElementById("message_container");
    setTimeout(function () {
        message_ele.style.display = "none";
    }, 4000);

}

function CheckDia(val) {
    console.log(val)
    let x = document.getElementsByClassName('menus')
    let i
    for (i = 0; i < x.length; i++) {
        let y = x[i]
        y.style.display= "none"
    }
    document.getElementById(val).style.display = ""
}