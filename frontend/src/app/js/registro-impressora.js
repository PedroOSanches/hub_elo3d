const carregarFilamentos = async () => {
    try{
        const response = await axios.get(
            `${API_BASE_URL}/filament/get_all`,
            {
                withCredentials: true
            }
        );
        const filamentos = response.data
        let filamentos_aceitos = document.getElementById('filamentos_aceitos')
        filamentos_aceitos.innerHTML = ""
        filamentos_aceitos.innerHTML = filamentos.map((filamento) => {
            return `
            <label class="check">
                <input type="checkbox" name="filamentos" value="${filamento.filament_id}">
                <span>${filamento.tipo}</span>
            </label>
            `
        }).join("");
    }
    catch{
        Error('Não foi possível carregar os tipos de filamentos',)
    }
}