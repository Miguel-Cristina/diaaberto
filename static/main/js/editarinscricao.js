function editar(area_estudos, escola, refeicaoaluno, refeicaooutro,
                tipotransporte, paracampus, qualcampus, entrecampus,
                entrecamposorigem) {
    // document.getElementById('id_area_estudos').value = area_estudos
    // document.getElementById('Escola').value = escola
    if (refeicaoaluno !== '0' || refeicaooutro !== '0') {
        document.getElementById('id_QuerRefeicao_0').checked = true
        document.getElementById('quer_refeicao').style.display = ''
    }else
        document.getElementById('id_QuerRefeicao_1').checked = true
    // document.getElementById('tipo_transporte').value = tipotransporte
    if (tipotransporte === 'autocarro' || tipotransporte === 'comboio') {
        document.getElementById('transporte_para_campus').style.display = ''
    }
    if (paracampus === 'sim') {
        document.getElementById('id_QuerTransportePara_0').checked = true
        document.getElementById('qual_campus').style.display = ''
    }
    document.getElementById('qual_campus_2').value = qualcampus
    if (entrecampus==='só ida'){
        document.getElementById('id_QuerTransporteEntre_0').checked = true
        document.getElementById('entre_campus').style.display='block'
        document.getElementById('timepicker-three_div').style.display='block'
    }else if (entrecampus==='ida e volta'){
        document.getElementById('id_QuerTransporteEntre_1').checked = true
        document.getElementById('entre_campus').style.display='block'
        document.getElementById('timepicker-three_div').style.display='block'
        document.getElementById('timepicker-four_div').style.display='block'
    }else if (entrecampus==='nao'){
        document.getElementById('id_QuerTransporteEntre_2').checked = true
    }
    if (entrecamposorigem==='penha'){
        document.getElementById('transporte_campus').value = 'penha_para_gambelas'
    }else if (entrecamposorigem==='gambelas'){
        document.getElementById('transporte_campus').value = 'gambelas_para_penha'
    }

}

function SessaoInitial(ses_id, val) {
    document.getElementById(ses_id).value = val
}