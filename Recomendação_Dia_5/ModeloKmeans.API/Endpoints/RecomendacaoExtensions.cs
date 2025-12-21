using ModeloKmeans.Models;
using ModeloKmeans.Converter;
using ModeloKmeans.Records;
using ModeloKmeans.Modifica;

namespace ModeloKmeans.Endpoints;

internal static class RecomendacaoExtensions
{
    public static void RecomendacaoEndpoint(this WebApplication app)
    {
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

        app.MapPut("/nova-avaliacao-usuario", (AvaliacaoRequest request) =>
        {
           Usuario? usuario = UsuarioConvert.ConverteRequestToUsuario(request);

           if (usuario is null)
            {
                return Results.NotFound("Usuário ou filme não existe");
            }

            JsonModifica.EscreveArquivoJson(usuario);
            return Results.Ok("Usuário atualizado");
        }).WithTags("Usuario");

        app.MapPost("/avaliacao-usuario-novo", (UsuarioRequest request) =>
        {
            Usuario? usuario = JsonModifica.DescerializaJson(request.Id);

            if (usuario is not null)
            {
                return Results.Conflict("Usuario já existe");
            }

            Usuario novoUsuario = UsuarioConvert.ConverteRequestToUsuario(request);

            if (novoUsuario is null)
            {
                return Results.NotFound("Filme não existe");
            }

            JsonModifica.EscreveArquivoJson(novoUsuario);
            return Results.Ok("Usuário criado");
        }).WithTags("Usuario");

        app.MapGet("/escreve-json", () =>
        {
            List<string> usuariosTexto = UsuarioModifica.LeArquivoAvaliacoes();
            Dictionary<int, List<string>> usuariosDict = UsuarioModifica.LeArquivoUsuario();
            UsuarioConvert.ConstroiArquivoJson(usuariosTexto, usuariosDict);
            return Results.Created();
        }).WithTags("Escreve-Arquivo");
    }
}