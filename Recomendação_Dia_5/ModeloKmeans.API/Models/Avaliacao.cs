namespace ModeloKmeans.Models;

internal class Avaliacao
{
    public int FilmeId { get; private set; }
    public int Nota { get; private set; }

    public Avaliacao(int FilmeId, int Nota)
    {
        this.FilmeId = FilmeId;
        this.Nota = Nota;
    }
}