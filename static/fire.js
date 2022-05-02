let fireContainer = document.getElementById("fire-container");
let smogContainer = document.getElementById("smog-container");
function createParticles(fireContainer, num, leftSpacing) {
  for (let i = 0; i < num; i += 1) {
    let particle = document.createElement("div");
    particle.style.left = `calc((100% - 5em) * ${i / leftSpacing })`;
    particle.setAttribute("class", "particle");
    particle.style.animationDelay = 4 * Math.random() + "s";
    fireContainer.appendChild(particle);
  }
}

createParticles(fireContainer, 60, 60);
createParticles(smogContainer, 30, 30);