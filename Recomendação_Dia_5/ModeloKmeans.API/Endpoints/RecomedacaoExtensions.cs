using ModeloKmeans.Models;
using ModeloKmeans.Converter;
using ModeloKmeans.Records;
using ModeloKmeans.Modifica;

namespace ModeloKmeans.Endpoints;

internal static class RecomendacaoExtensions
{
    public static void RecomendacaoEndpoint(this WebApplication app)
    {
        // Usuario Filme

        app.MapGet("/lista-usuarios", () =>
        {
            var listaUsuario = UsuarioConvert.ConverteRequestToListUsuario()!.ToList();
            return Results.Ok(listaUsuario);
        }).WithTags("Usuario");

        app.MapGet("/usuario/{id}", (int id) =>
        {
            Usuario? usuario = JsonModifica.DescerializaJson(id);

            if (usuario is null)
            {
                return Results.NotFound("Usuário não existe");
            }

            return Results.Ok(usuario);
        }).WithTags("Usuario");

        app.MapGet("/escreve-json", () =>
        {
            List<string> usuariosTexto = UsuarioModifica.LeArquivoFilme();
            Dictionary<int, List<string>> usuariosDict = UsuarioModifica.LeArquivoUsuario();
            UsuarioConvert.ConstroiArquivoJson(usuariosTexto, usuariosDict);
            return Results.Created();
        }).WithTags("Usuario");

        app.MapPost("/avaliacao-usuario", (UsuarioRequest request) =>
        {
            Usuario usuario = UsuarioConvert.ConverteRequestToUsuario(request);
            JsonModifica.EscreveArquivoJson(usuario);
            return Results.Ok();
        }).WithTags("Usuario");
    }
}