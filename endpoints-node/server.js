// Para poder importar un package.json con Import
// hay que usar "Type": "Module"

import express from "express";

const app = express();
const PORT = 5000;

app.get("/", (req, res) => {
  res.send("Este es un endpoint hecho con express");
});

// Endpoint con párametro.
app.get("/api/user/:id", (req, res) => {
  //destructuración
  const { id } = req.params;
  res.send({ message: `El usuario con id ${id} es Juan` });
});

// Query Params
app.get("/api/search", (req, res) => {
  const { name, lastname } = req.query;
  res.json({
    firstName: name,
    lastname,
  });
  //http://localhost:5000/api/search?name=Juan&lastname=Manuel
  // No debe usar el protocolo https si no http.
});

// Ruta de POST.

app.post("/api/user", (req, res) => {
  const { name, email } = req.body;
  res.json({ message: "Usuario creado", data: { name, email } });
  // Para probar este endpoint hay que usar Postman.
  // Dado que requiere de un POST.
});

app.listen(PORT, () => {
  console.log(`Servidor corriendo en el puerto ${PORT}`);
});
