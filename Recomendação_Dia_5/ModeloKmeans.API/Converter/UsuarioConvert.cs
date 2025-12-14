using ModeloKmeans.Models;
using ModeloKmeans.Records;
using ModeloKmeans.Modifica;

namespace ModeloKmeans.Converter;

internal static class UsuarioConvert
{

    private static Usuario CriaUsuario(UsuarioRequest request)
    {
        var lista = new List<Avaliacao>
        {
            new Avaliacao(request.FilmeId, request.Nota)
        };

        return new Usuario(request.Id, lista, request.Idade, request.Genero);
    }

    public static Usuario ConverteRequestToUsuario(UsuarioRequest request)
    {
        var usuario = JsonModifica.DescerializaJson(request.Id);

        if (usuario is not null)
        {
            var filme = usuario.Avaliacao.FirstOrDefault(filme => filme.FilmeId == request.FilmeId);
            
            if (filme is not null)
            {
                return usuario;
            }

            List<Avaliacao> listaAvaliacoes = usuario.Avaliacao.ToList();
            Avaliacao avaliacao = new Avaliacao(request.FilmeId, request.Nota);

            listaAvaliacoes.Add(avaliacao);
            listaAvaliacoes = listaAvaliacoes.OrderBy(filme => filme.FilmeId).ToList();

            usuario.Avaliacao = listaAvaliacoes;

            return usuario;
        }

        return CriaUsuario(request);
    }

    public static void ConstroiArquivoJson(List<string> usuariosFilmesTexto,  Dictionary<int, List<string>> usuariosDict)
    {
       var usuariosTextoDict = new Dictionary<int, Usuario>();

        foreach (var texto in usuariosFilmesTexto)
        {
            string[] partes = texto.Replace("\t", ",").Trim().Split(',');

            int id = int.Parse(partes[0]);
            int filmeId = int.Parse(partes[1]);
            int nota = int.Parse(partes[2]);

            List<string> atributos = usuariosDict[id];

            int idade = int.Parse(atributos[0]);
            string genero = atributos[1];

            if (!usuariosTextoDict.TryGetValue(id, out var usuario))
            {
                usuario = new Usuario(id, new List<Avaliacao>(), idade, genero);
                usuariosTextoDict[id] = usuario;
            }

            var avaliacoes = usuario.Avaliacao.ToList();
            avaliacoes.Add(new Avaliacao(filmeId, nota));
            usuario.Avaliacao = avaliacoes;
        }

        var listaUsuarios = usuariosTextoDict.Values.OrderBy(usuario => usuario.Id).ToList();
        JsonModifica.EscreveArquivoJson(listaUsuarios);
    }

    public static IEnumerable<Usuario>? ConverteRequestToListUsuario() => JsonModifica.DescerializaJson();
}
