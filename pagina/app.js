document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:8000/placas/')
        .then(response => response.json())
        .then(data => {
            const contenedor = document.getElementById('contenedor-placas');
            const row = document.createElement('div');
            row.classList.add('row', 'align-items-stretch', 'justify-content-between');
            data.forEach(placa => {
                const col = document.createElement('div');
                col.classList.add('col-lg-3','m-1','p-3'); 
                const article = document.createElement('article');
                article.classList.add('producto','row')
                article.innerHTML = `
                    <img alt="${placa.Nombre}" class="imagen-placa img-fluid" src="data:image/jpeg;base64,${placa.Imagen}">
                    <h3>${placa.Nombre}</h3>
                    <p>Marca: ${placa.Marca}</p>
                    <p>Precio: $${placa.Precio}</p>
                    <p>Tienda: ${placa.Tienda}</p>
                    <button><a href="${placa.Link}" target="_blank">${placa.Nombre} en ${placa.Tienda}</a></button>
                `;
                col.appendChild(article);
                row.appendChild(col);
            });
            contenedor.appendChild(row);
        })
        .catch(error => console.error(error));
});

/*Buscar una placa por el nombre*/ 
const boton = document.getElementById('btnBuscar');
const input = document.getElementById('inputBuscar');

input.addEventListener('input', function(event) {
    event.preventDefault();
    const nombrePlaca = input.value;
    fetch(`http://127.0.0.1:8000/placas?nombre=${nombrePlaca}`)

        .then(response => response.json())
        .then(data => {
            const contenedor = document.getElementById('contenedor-placas');

            while (contenedor.firstChild) {
                contenedor.removeChild(contenedor.firstChild);
            }

            const row = document.createElement('div');
            row.classList.add('row', 'align-items-stretch', 'justify-content-between');
            data.forEach(placa => {
                const col = document.createElement('div');
                col.classList.add('col-lg-3','m-2','p-2'); 
                const article = document.createElement('article');
                article.classList.add('producto','row')
                article.innerHTML = `
                    <img alt="${placa.Nombre}" class="imagen-placa img-fluid" src="data:image/jpeg;base64,${placa.Imagen}">
                    <h3>${placa.Nombre}</h3>
                    <p>Marca: ${placa.Marca}</p>
                    <p>Precio: $${placa.Precio}</p>
                    <p>Tienda: ${placa.Tienda}</p>
                    <button><a href="${placa.Link}" target="_blank">${placa.Nombre} en ${placa.Tienda}</a></button>
                `;
                col.appendChild(article);
                row.appendChild(col);
            });
            contenedor.appendChild(row);

        })
        .catch(error => console.error(error));
});





/*Agregar una placa a la base de datos*/
productForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const productName = document.getElementById("productName").value;
    const productPrice = document.getElementById("productPrice").value;
    const productLink = document.getElementById("productLink").value;
    const productBrand = document.getElementById("productBrand").value;
    const productStore = document.getElementById("productStore").value;

    const selectedImageFile = productImageInput.files[0];


    const productData = {
        productName,
        productPrice,
        productLink,
        productBrand,
        productStore,
    };

    const formData = new FormData();
    formData.append("productImage", selectedImageFile);


    formData.append("productData", JSON.stringify(productData));

 
    try {
        const response = await fetch("http://127.0.0.1:8000/post_placa/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json", 
            },
            body: JSON.stringify({ productData }),
        });

        if (response.ok) {
            console.log("Producto agregado exitosamente.");
            productForm.reset();
        } else {
            console.error("Error al agregar el producto.");
        }
    } catch (error) {
        console.error("Error de conexión:", error);
    }
});


/*Filtro por marca*/

const opciones = document.getElementsByName('opcion');
for (let i = 0; i < opciones.length; i++) {
    opciones[i].addEventListener('change', function () {
        if (opciones[i].checked) {
            const opcionMarcada = opciones[i].value;
            fetch(`http://127.0.0.1:8000/placas?nombre=${nombrePlaca}`)

            .then(response => response.json())
            .then(data => {
                const contenedor = document.getElementById('contenedor-placas');

                while (contenedor.firstChild) {
                    contenedor.removeChild(contenedor.firstChild);
                }

                const row = document.createElement('div');
                row.classList.add('row', 'align-items-stretch', 'justify-content-between');
                data.forEach(placa => {
                    const col = document.createElement('div');
                    col.classList.add('col-lg-3','m-2','p-2'); 
                    const article = document.createElement('article');
                    article.classList.add('producto','row')
                    article.innerHTML = `
                        <img alt="${placa.Nombre}" class="imagen-placa img-fluid" src="data:image/jpeg;base64,${placa.Imagen}">
                        <h3>${placa.Nombre}</h3>
                        <p>Marca: ${placa.Marca}</p>
                        <p>Precio: $${placa.Precio}</p>
                        <p>Tienda: ${placa.Tienda}</p>
                        <button><a href="${placa.Link}" target="_blank">${placa.Nombre} en ${placa.Tienda}</a></button>
                    `;
                    col.appendChild(article);
                    row.appendChild(col);
                });
                contenedor.appendChild(row);

            })
            .catch(error => console.error(error));
            }
        });
}




