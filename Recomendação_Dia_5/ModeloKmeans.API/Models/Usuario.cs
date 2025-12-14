namespace ModeloKmeans.Models;

internal class Usuario
{
    private int id;
    private int idade;
    private string genero;
    private IEnumerable<Avaliacao> avaliacao;

    public int Id
    {
        get
        {
            return id;
        }

        private set
        {
            id = value;
        }
    }
    
    public int Idade
    {

        get
        {
            return idade;
        }

        set
        {
            idade = value;
        }
    }
    
    public string Genero
    {

        get
        {
            return genero;
        }

        set
        {
            genero = value;
        }
    }
    
    public IEnumerable<Avaliacao> Avaliacao
    {

        get
        {
            return avaliacao;
        }

        set
        {
            avaliacao = value;
        }
    }
    

    public Usuario(int Id, IEnumerable<Avaliacao> Avaliacao, int Idade, string Genero)
    {
        this.Id = Id;
        this.Avaliacao = Avaliacao;
        this.Idade = Idade;
        this.Genero = Genero;
    }
}