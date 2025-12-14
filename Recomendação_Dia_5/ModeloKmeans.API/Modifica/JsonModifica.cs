using System.Collections;
using System.Text.Json;
using ModeloKmeans.Models;
using ModeloKmeans.Records;

namespace ModeloKmeans.Modifica;

internal static class JsonModifica
{
    private static string caminhoUsuarioData = @"H:\GitHub\Python\7DaysOfCode\Ciência de Dados\Recomendação_Dia_5\usuarios_data.json";
    private static List<Usuario>? listaUsuario = LeArquivoJson(caminhoUsuarioData);

    //private static string caminhoUsuario= @"H:\GitHub\Python\7DaysOfCode\Ciência de Dados\Recomendação_Dia_5\usuarios.json";
    //private static List<Usuario>? listaUsuario = LeArquivo(@"H:\GitHub\Python\7DaysOfCode\Ciência de Dados\Recomendação_Dia_5\usuarios.json");

    private static List<Usuario>? LeArquivoJson(string caminho)
    {
        List<Usuario>? usuarios = null;

        try
        {
            using (StreamReader sr = new StreamReader(caminho))
            {
                var texto = sr.ReadToEnd();

                usuarios = JsonSerializer.Deserialize<List<Usuario>>(texto);
            }
            
        }
        catch (Exception exception)
        {
            Console.WriteLine($"O arquivo não existe. Criando um no lugar: {exception.Message}");

            File.WriteAllText(caminho,"");
        }

        return usuarios;
    }

    public static void EscreveArquivoJson(Usuario usuario)
    {
        if (listaUsuario is null)
        {
            listaUsuario = new List<Usuario>();
        }

        int index = -1;

        foreach (var usuarioLista in listaUsuario)
        {
            if (usuarioLista.Id == usuario.Id)
            {
                index = listaUsuario.IndexOf(usuarioLista);
            }
        }

        if (index != -1)
        {
            List<Avaliacao> listaSubstitutiva = (List<Avaliacao>)listaUsuario[index].Avaliacao;

            foreach (var filme in usuario.Avaliacao)
            {
                if (!listaSubstitutiva.Contains(filme))
                {
                    listaSubstitutiva.Add(filme);
                }
            }

            listaUsuario[index].Avaliacao = listaSubstitutiva;
        }
        else
        {
            listaUsuario.Add(usuario);
        }


        using (StreamWriter sw = new StreamWriter(@"H:\GitHub\Python\7DaysOfCode\Ciência de Dados\Recomendação_Dia_5\usuarios_data.json"))
        {
            var texto = JsonSerializer.Serialize(listaUsuario);
            sw.Write(texto);
        }
    }

    public static void EscreveArquivoJson(List<Usuario> listaUsuarios)
    {
        using (StreamWriter sw = new StreamWriter(@"H:\GitHub\Python\7DaysOfCode\Ciência de Dados\Recomendação_Dia_5\usuarios_data.json"))
        {
            var texto = JsonSerializer.Serialize(listaUsuarios);
            sw.Write(texto);
        }
    }
    
    public static Usuario? DescerializaJson(int id)
    {
        if (listaUsuario is not null)
        {
            foreach (var usuario in listaUsuario)
            {
                if (usuario.Id == id)
                {
                    return new Usuario(id, [..usuario.Avaliacao], usuario.Idade, usuario.Genero);
                }
            }
        }

        return null;
    }

    public static IEnumerable<Usuario>? DescerializaJson() => [..listaUsuario];
    
}