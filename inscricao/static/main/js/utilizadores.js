function confirmacao(id, value) {
    if (id === "apagar"){
    document.getElementById('popup_eliminar_utilizador').style.display = ''
    document.getElementById('type').value=1
    document.getElementById('del').value=value
    }else if (id === "popup_eliminar_utilizador"){
        document.getElementById('popup_eliminar_utilizador').style.display = 'none'
    }else if (id === "validar"){
        document.getElementById('popup_validar').style.display = ''
        document.getElementById('type').value=0
        document.getElementById('val').value=value
    }else if (id === "popup_validar"){
        document.getElementById('popup_validar').style.display = 'none'
    }
}

