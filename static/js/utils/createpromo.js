//promociones
const publidata = {
  title: "Zapatillas",
  image1:"static/images/png/promocion/1a.png",
  image2: "static/images/png/promocion/1.png",
  image3: "static/images/png/promocion/2.png",
  image4: "static/images/png/promocion/3.png",
  image5: "static/images/png/promocion/4.png",
};

const publidata2 = {
  title: "Zapatillas para correr",
  image1:"https://http2.mlstatic.com/D_NQ_931465-MLA79507656698_102024-OO.webp",
  image2: "static/images/png/promocion/1.png",
  image3: "static/images/png/promocion/2.png",
  image4: "static/images/png/promocion/3.png",
  image5: "static/images/png/promocion/4.png",
};

const publidata3 = {
  title: "Zapatillas para mamá",
  image1:"https://http2.mlstatic.com/D_NQ_931465-MLA79507656698_102024-OO.webp",
  image2: "static/images/png/promocion/1.png",
  image3: "static/images/png/promocion/2.png",
  image4: "static/images/png/promocion/3.png",
  image5: "static/images/png/promocion/4.png",
};

const publidata4 = {
    title: "Zapatillas para mamá",
    image1:"https://http2.mlstatic.com/D_NQ_931465-MLA79507656698_102024-OO.webp",
    image2: "static/images/png/promocion/1.png",
    image3: "static/images/png/promocion/2.png",
    image4: "static/images/png/promocion/3.png",
    image5: "static/images/png/promocion/4.png",
};

const publidata5 = {
    title: "Zapatillas para mamá",
    image1:"https://http2.mlstatic.com/D_NQ_931465-MLA79507656698_102024-OO.webp",
    image2: "static/images/png/promocion/1.png",
    image3: "static/images/png/promocion/2.png",
    image4: "static/images/png/promocion/3.png",
    image5: "static/images/png/promocion/4.png",
};
const publidata6 = {
    title: "Zapatillas para mamá",
    image1:"https://http2.mlstatic.com/D_NQ_931465-MLA79507656698_102024-OO.webp",
    image2: "static/images/png/promocion/1.png",
    image3: "static/images/png/promocion/2.png",
    image4: "static/images/png/promocion/3.png",
    image5: "static/images/png/promocion/4.png",
};

//agregar mas promociones 

function createpubli(publi) {
  return `
        <div style="width: 300px; background: white; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); overflow: hidden;">
            <h2 style="padding: 16px;">
                <a href="#" style="text-decoration: none; color: #1F2937;">
                    <p style="font-size: 1.5rem; font-weight: bold;">${publi.title}</p>
                </a>
            </h2>
            <div style="position: relative;">
                <img src="${publi.image1}"
                    alt="Las mejores ofertas en ZAPATILLAS"
                    style="width: 100%; height: 180px; object-fit: cover; transition: transform 0.3s;"
                    class="hover:scale-110">
            </div>
            <div style="padding: 16px;">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                    <a href="#">
                        <img src="${publi.image2}" alt="Zapatillas Deportivas"
                            style="width: 80px; height: 80px; object-fit: contain; border-radius: 8px; transition: transform 0.3s;"
                            class="hover:scale-110">
                    </a>
                    <a href="#">
                        <img src="${publi.image3}" alt="Zapatillas Deportivas"
                            style="width: 80px; height: 80px; object-fit: contain; border-radius: 8px; transition: transform 0.3s;"
                            class="hover:scale-110">
                    </a>
                    <a href="#">
                        <img src="${publi.image4}" alt="Zapatillas Deportivas"
                            style="width: 80px; height: 80px; object-fit: contain; border-radius: 8px; transition: transform 0.3s;"
                            class="hover:scale-110">
                    </a>
                    <a href="#">
                        <img src="${publi.image5}" alt="Zapatillas Deportivas"
                            style="width: 80px; height: 80px; object-fit: contain; border-radius: 8px; transition: transform 0.3s;"
                            class="hover:scale-110">
                    </a>
                </div>
            </div>
        </div>`;
}

// Insertar la publicación en el contenedor
document.getElementById("contenedor-publicaciones").innerHTML = createpubli(publidata);
document.getElementById("contenedor-publicaciones2").innerHTML = createpubli(publidata2);
document.getElementById("contenedor-publicaciones3").innerHTML = createpubli(publidata3);
document.getElementById("contenedor-publicaciones4").innerHTML = createpubli(publidata4);
document.getElementById("contenedor-publicaciones5").innerHTML = createpubli(publidata5);
document.getElementById("contenedor-publicaciones6").innerHTML = createpubli(publidata6);

//segun vayan agregando aumenten el numero de contenedor-publicaciones y de  publidata