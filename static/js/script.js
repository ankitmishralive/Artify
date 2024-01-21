


var aText = new Array(
  "Unlock the Potential of Your Documents with DocBerg: Reshape Resumes,Visualize Chats,Effortless Compression, PDF Mastery, Multilingual Audio, and Streamlined Format Conversions & much more undercover. ",
  );


  // var aText = new Array(
  //   "  Your Document Mastery Redefined Here."   
  //  );

  var iSpeed = 30; // time delay of print out
  var iIndex = 0; // start printing array at this posision
  var iArrLength = aText[0].length; // the length of the text array
  var iScrollAt = 20; // start scrolling up at this many lines
   
  var iTextPos = 0; // initialise text position
  var sContents = ''; // initialise contents variable
  var iRow; // initialise current row

function typewriter() {
    sContents = '';
    iRow = Math.max(0, iIndex - iScrollAt);
    var destination = document.getElementById("typedtext2");
  
    while (iRow < iIndex) {
      sContents += aText[iRow++] + '<br />';
    }
    destination.innerHTML = sContents + aText[iIndex].substring(0, iTextPos) + "|";
    if (iTextPos++ == iArrLength) {
      if (iIndex == aText.length - 1) {
        // Reset the index and text position to restart the animation
        iIndex = 0;
        iTextPos = 0;
      } else {
        iIndex++;
      }
      iArrLength = aText[iIndex].length;
    }
    setTimeout(typewriter, iSpeed);
  }
  
  // Initial call to start the typewriter animation
  // typewriter();


//   function toggleNav() {
//     const navLinksMobile = document.getElementById('navLinksMobile');
//     navLinksMobile.classList.toggle('hidden');
// }




//------------------


// document.addEventListener('DOMContentLoaded', function () {
//   const cardSlider = document.getElementById('cardSlider');
//   const cards = document.querySelectorAll('.card');
//   let currentIndex = 0;

//   function showCard(index) {
//       cards.forEach(card => card.classList.remove('active'));
//       cards[index].classList.add('active');
//   }

//   function nextCard() {
//       currentIndex = (currentIndex + 1) % cards.length;
//       showCard(currentIndex);
//   }

//   // Initial display
//   showCard(currentIndex);

//   // Auto slide every 5 seconds (adjust as needed)
//   setInterval(nextCard, 3000);
// });



// New Header js 

document.addEventListener('DOMContentLoaded', function () {
  const mobileMenuButton = document.getElementById('mobile-menu-button');
  const mobileNav = document.getElementById('mobile-nav');

  mobileMenuButton.addEventListener('click', function () {
      mobileNav.classList.toggle('hidden');
  });
});

document.addEventListener('DOMContentLoaded', function () {
  console.log('DOMContentLoaded event triggered');
  
  const sliderContainer = document.getElementById('cardSlide');
  console.log('sliderContainer:', sliderContainer);

  const cards = document.querySelectorAll('.card');
  console.log('cards:', cards);

  let currentIndex = 0;
  let sliderInterval;

  function showCard(index) {
    console.log('Showing card:', index);
    cards.forEach(card => card.classList.remove('active'));
    cards[index].classList.add('active');
  }

  function nextCard() {
    console.log('Moving to next card');
    currentIndex = (currentIndex + 1) % cards.length;
    showCard(currentIndex);

    // Optional: Stop sliding when reaching the last card
    if (currentIndex === 0) {
      clearInterval(sliderInterval);
      console.log('Slider stopped');
    }
  }

  // Initial display
  showCard(currentIndex);
  console.log('Initial display');

  // Auto slide every 5 seconds (adjust as needed)
  sliderInterval = setInterval(nextCard, 3000);
  console.log('Slider interval set');
});


// 


function moveToTools() {
  // const element = document.getElementById('allTools');

  // if (element) {
  //   element.scrollIntoView({ behavior: 'smooth' });
  // }
  window.location.href="/features"
}
