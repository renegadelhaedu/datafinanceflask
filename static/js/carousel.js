let count = 1;

        document.getElementById("radio1").checked = true;

        function nextImage(){
            count++;
            if(count > 4){
                count = 1;
                document.querySelector('.slides').style.transition = 'none';
                document.querySelector('.slides').style.transform = 'translateX(0)';
                setTimeout(function(){
                    document.querySelector('.slides').style.transition = 'transform 2s ease-in-out';
                }, 50);
            }
            document.getElementById("radio"+count).checked = true;
        }

        document.querySelector('.slides').addEventListener('transitionend', function(){
            nextImage();
        });

        function startTransition() {
            setInterval(function() {
                document.querySelector('.slides').style.transform = 'translateX(' + (-100 * count) + '%)';
            }, 0); //tempo para iniciar
        }

        window.onload = startTransition;