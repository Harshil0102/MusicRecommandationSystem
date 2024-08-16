console.log("Rockerzz");

// Initialize the Variables
let songIndex = 0;
let audioElement = new Audio ("/Content/Allsongs/1.mp3");
let masterPlay = document.getElementById("masterPlay");
let myProgressBar = document.getElementById("myProgressBar");
let  gif = document.getElementById("gif");
let songItems = Array.from(document.getElementsByClassName('songItems'));

let songs = [
    {songName:"Starboy - The Weekend", filePath:"/Content/Allsongs/1.mp3", coverPath:"/Content/covers/1.png"},
    {songName:"Beautiful - Michele Morrone", filePath:"/Content/Allsongs/2.mp3", coverPath:"/Content/covers/2.jpg"},
    {songName:"I Warned Myself - Charlie Puth", filePath:"/Content/Allsongs/3.mp3", coverPath:"/Content/covers/3.jpg"},
    {songName:"As it Was - Harry Styles", filePath:"/Content/Allsongs/4.mp3", coverPath:"/Content/covers/4.jpg"},
    {songName:"Dandelions - Ruth B.", filePath:"/Content/Allsongs/5.mp3", coverPath:"/Content/covers/5.jpg"},
    {songName:"Still Don't Know My Name - Labrith", filePath:"/Content/Allsongs/6.mp3", coverPath:"/Content/covers/6.jpg"},
    {songName:"Late Night Talking - Harry Styles", filePath:"/Content/Allsongs/7.mp3", coverPath:"/Content/covers/7.jpg"},
    {songName:"We Rollin - Shubh", filePath:"/Content/Allsongs/8.mp3", coverPath:"/Content/covers/8.jpg"},
    {songName:"No Love - Shubh", filePath:"/Content/Allsongs/9.mp3", coverPath:"/Content/covers/9.jpg"},
    {songName:"Double Take - Dhruv", filePath:"/Content/Allsongs/10.mp3", coverPath:"/Content/covers/10.jpg"},
    {songName:"See You Again - Wiz Khalifa ft.Charlie Puth", filePath:"/Content/Allsongs/11.mp3", coverPath:"/Content/covers/11.jpg"},
    {songName:"Steal My Girl - One Direction", filePath:"/Content/Allsongs/12.mp3", coverPath:"/Content/covers/12.jpg"},
    {songName:"Summer of Love - Shawn Mendes", filePath:"/Content/Allsongs/13.mp3", coverPath:"/Content/covers/13.jpg"}
]

songItems.forEach((element, i ) => {
    console.log(element, i);
    element.getElementsByTagName("img")[0].src = songs[i].coverPath;
    element.getElementsByClassName("songName")[0].innerText = songs[i].songName;
    
})

// HAndle Play/Pause Event
masterPlay.addEventListener('click', ()=>{
    if(audioElement.paused || audioElement.currentTime <= 0){
    audioElement.play();
    masterPlay.classList.remove("fa-play-circle");
    masterPlay.classList.add("fa-pause-circle");
    gif.style.opacity = 1;
    }
    
    else{
        audioElement.pause();
    audioElement.pause();
    masterPlay.classList.add("fa-play-circle");
    masterPlay.classList.remove("fa-pause-circle");
    gif.style.opacity = 0;
    }

});


// Listen To Event
audioElement.addEventListener('timeupdate', ()=>{
    // Update SeekBar
   progress =parseInt((audioElement.currentTime/audioElement.duration)*100);
   myProgressBar.value = progress;
});

// change Seekbar
myProgressBar.addEventListener('change', ()=>{
    audioElement.currentTime = myProgressBar.value * audioElement.duration/100;
});

//Play with screen play button along with song 
const makeAllPlays = () =>{
    Array.from(document.getElementsByClassName('songItemsPlay')).forEach((element)=>{
        element.classList.remove("fa-pause-circle");
        element.classList.add('fa-play-circle');
    })
} 

Array.from(document.getElementsByClassName('songItemsPlay')).forEach((element)=>{
    element.addEventListener('click', (e)=>{
        makeAllPlays();
        songIndex = parseInt(e.target.id);
        e.target.classList.remove('fa-play-circle');
        e.target.classList.add('fa-pause-circle');
        audioElement.src =`Content/Allsongs/${songIndex+1}.mp3`;
        masterSongName.innerText = songs[songIndex].songName;
        audioElement.currentTime = 0; 
        audioElement.play();
        masterPlay.classList.remove("fa-play-circle");
        masterPlay.classList.add("fa-pause-circle");
        gif.style.opacity=1;
    })
}) 

// playing Next Song
document.getElementById("next").addEventListener('click', ()=>{
    if(songIndex>=12){
        songIndex = 0;
    }
    else{
        songIndex += 1;
    }
    audioElement.src =`Content/Allsongs/${songIndex + 1}.mp3`;
    masterSongName.innerText = songs[songIndex].songName;
    audioElement.currentTime = 0; 
    audioElement.play();
    masterPlay.classList.remove("fa-play-circle");
    masterPlay.classList.add("fa-pause-circle");
    gif.style.opacity=1;
})

// playing Previous Song
document.getElementById("previous").addEventListener('click', ()=>{
    if(songIndex<=0){
        songIndex = 12;
    }
    else{
        songIndex -= 1;
    }
    audioElement.src =`Content/Allsongs/${songIndex+1}.mp3`;
    masterSongName.innerText = songs[songIndex].songName;
    audioElement.currentTime = 0; 
    audioElement.play();
    masterPlay.classList.remove("fa-play-circle");
    masterPlay.classList.add("fa-pause-circle");
    gif.style.opacity=1;
})







