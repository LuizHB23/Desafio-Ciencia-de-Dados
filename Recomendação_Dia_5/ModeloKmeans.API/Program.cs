using System.Text.Json.Serialization;
using ModeloKmeans.Endpoints;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<Microsoft.AspNetCore.Http.Json.JsonOptions>(options => options.SerializerOptions.ReferenceHandler = ReferenceHandler.IgnoreCycles);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();


var app = builder.Build();

app.RecomendacaoEndpoint();

app.UseSwagger();
app.UseSwaggerUI();


app.Run();
