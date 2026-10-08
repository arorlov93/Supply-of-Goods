dots = open("am/dots.txt").read()

globe = r'''<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<script defer crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded',function(){
(function(){
  /* Глобус на three.js. Точки суши взяты из контуров Natural Earth 110m:
     равномерная по площади решётка Фибоначчи, проверка «точка внутри полигона»,
     4183 точки, упакованы по три символа base64 на координату, 12 КБ. */
  var DOTS = "''' + dots + r'''";
  var B="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-";
  var IDX={}; for (var i=0;i<64;i++) IDX[B[i]]=i;

  var cv = document.getElementById('globe');
  if (!cv || typeof THREE === 'undefined') return;

  var css=function(n){ return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var C_LAND = new THREE.Color(css('--brand')   || '#116b5c');
  var C_DOT  = new THREE.Color('#06302a');
  var C_SEA  = new THREE.Color('#bfd5cd');
  var C_SEA2 = new THREE.Color('#467a6e');
  var C_GOLD = new THREE.Color(css('--gold')    || '#b8862b');

  var R = 1;
  function v3(lat,lon,r){
    var a=lat*Math.PI/180, b=lon*Math.PI/180, c=Math.cos(a);
    return new THREE.Vector3(c*Math.cos(b)*(r||R), Math.sin(a)*(r||R), c*Math.sin(b)*(r||R));
  }

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(0, 0.62, 3.25);
  camera.lookAt(0,0,0);
  var renderer = new THREE.WebGLRenderer({canvas:cv, alpha:true, antialias:true});
  renderer.setClearColor(0x000000, 0);

  var world = new THREE.Group();
  world.rotation.z = -0.36;
  scene.add(world);

  /* океан: мягкая растушёвка от освещённой стороны к терминатору */
  var sea = new THREE.Mesh(
    new THREE.SphereGeometry(R*0.995, 72, 48),
    new THREE.ShaderMaterial({
      uniforms:{ cA:{value:C_SEA}, cB:{value:C_SEA2} },
      vertexShader:'varying vec3 vN; void main(){ vN=normalize(normalMatrix*normal);'+
        ' gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
      fragmentShader:'uniform vec3 cA; uniform vec3 cB; varying vec3 vN;'+
        ' void main(){ float l=clamp(dot(vN,normalize(vec3(-0.55,0.62,0.78)))*0.5+0.5,0.0,1.0);'+
        ' gl_FragColor=vec4(mix(cB,cA,pow(l,1.75)),1.0); }'
    })
  );
  world.add(sea);

  /* атмосфера: френель по задней грани */
  var atmo = new THREE.Mesh(
    new THREE.SphereGeometry(R*1.19, 64, 42),
    new THREE.ShaderMaterial({
      uniforms:{ c:{value:C_LAND} }, side:THREE.BackSide, transparent:true,
      blending:THREE.NormalBlending, depthWrite:false,
      vertexShader:'varying vec3 vN; varying vec3 vP; void main(){ vN=normalize(normalMatrix*normal);'+
        ' vec4 mv=modelViewMatrix*vec4(position,1.0); vP=mv.xyz;'+
        ' gl_Position=projectionMatrix*mv; }',
      fragmentShader:'uniform vec3 c; varying vec3 vN; varying vec3 vP;'+
        ' void main(){ float f=pow(clamp(1.0-abs(dot(normalize(vN),normalize(-vP))),0.0,1.0),2.6);'+
        ' gl_FragColor=vec4(c, f*0.34); }'
    })
  );
  world.add(atmo);

  /* точки суши */
  var n = DOTS.length/3, pos = new Float32Array(n*3), ph = new Float32Array(n);
  for (var k=0;k<n;k++){
    var v = (IDX[DOTS[k*3]]<<12) | (IDX[DOTS[k*3+1]]<<6) | IDX[DOTS[k*3+2]];
    var xi = v % 720, yi = (v - xi)/720;
    var lon = xi/2 - 180, lat = yi/2 - 90;
    var p = v3(lat, lon, R*1.004);
    pos[k*3]=p.x; pos[k*3+1]=p.y; pos[k*3+2]=p.z;
    ph[k] = lon;
  }
  var g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos,3));
  g.setAttribute('aLon', new THREE.BufferAttribute(ph,1));

  /* круглый спрайт точки, рисуем сами, чтобы не тянуть картинку */
  var dc = document.createElement('canvas'); dc.width=dc.height=64;
  var dx = dc.getContext('2d');
  var rg = dx.createRadialGradient(32,32,0,32,32,32);
  rg.addColorStop(0,'rgba(255,255,255,1)'); rg.addColorStop(0.45,'rgba(255,255,255,0.95)');
  rg.addColorStop(1,'rgba(255,255,255,0)');
  dx.fillStyle=rg; dx.beginPath(); dx.arc(32,32,32,0,6.2832); dx.fill();
  var sprite = new THREE.CanvasTexture(dc);

  var dotMat = new THREE.ShaderMaterial({
    uniforms:{ uT:{value:0}, uC:{value:C_DOT}, uG:{value:C_GOLD}, uTex:{value:sprite},
               uPR:{value:1}, uSize:{value:5.2} },
    transparent:true, depthWrite:false,
    vertexShader:
      'attribute float aLon; uniform float uT; uniform float uPR; uniform float uSize;'+
      'varying float vW; varying float vFront;'+
      'void main(){'+
      ' vec4 mv=modelViewMatrix*vec4(position,1.0);'+
      ' vec3 nw=normalize((modelViewMatrix*vec4(position,0.0)).xyz);'+
      ' vFront=smoothstep(-0.15,0.35,dot(nw,normalize(-mv.xyz)));'+
      /* волна бежит по долготе, точки на её гребне крупнее и золотистее */
      ' float w=sin((aLon*0.0349)-uT*3.4);'+
      ' vW=smoothstep(0.86,1.0,w);'+
      ' gl_PointSize=(uSize+vW*4.2)*uPR*(2.2/-mv.z);'+
      ' gl_Position=projectionMatrix*mv; }',
    fragmentShader:
      'uniform sampler2D uTex; uniform vec3 uC; uniform vec3 uG;'+
      'varying float vW; varying float vFront;'+
      'void main(){ vec4 t=texture2D(uTex, gl_PointCoord);'+
      ' if(t.a<0.08) discard;'+
      ' vec3 c=mix(uC,uG,vW*0.85);'+
      ' gl_FragColor=vec4(c, t.a*(0.10+vFront*0.90)*(0.80+vW*0.20)); }'
  });
  world.add(new THREE.Points(g, dotMat));

  /* маршруты */
  var ports = [[38.4,27.1],[41.0,29.0],[54.4,18.7],[51.9,4.1],[29.8,-95.4],[25.8,-80.2],
    [-24.0,-46.3],[-33.0,-71.6],[6.1,1.2],[6.4,2.4],[-29.9,31.0],[19.1,72.9],[29.9,121.8],[68.9,33.1]]
    .map(function(p){ return v3(p[0],p[1],R*1.012); });
  var lanes=[[0,5],[1,4],[6,8],[7,9],[2,8],[10,11],[4,9],[12,3],[12,13],[11,10],[12,5]];
  var movers=[];
  lanes.forEach(function(L,li){
    var a=ports[L[0]], b=ports[L[1]];
    var pts=[], SEG=128;
    for (var s=0;s<=SEG;s++){
      var t=s/SEG;
      var p=new THREE.Vector3().copy(a).lerp(b,t).normalize()
             .multiplyScalar(R*(1.012+0.21*Math.sin(Math.PI*t)));
      pts.push(p);
    }
    var cg=new THREE.BufferGeometry().setFromPoints(pts);
    var cols=new Float32Array(pts.length*3);
    for (var q=0;q<pts.length;q++){
      var f=Math.sin(Math.PI*(q/(pts.length-1)));
      cols[q*3]=C_LAND.r*(0.45+f*0.55); cols[q*3+1]=C_LAND.g*(0.45+f*0.55); cols[q*3+2]=C_LAND.b*(0.45+f*0.55);
    }
    cg.setAttribute('color', new THREE.BufferAttribute(cols,3));
    world.add(new THREE.Line(cg, new THREE.LineBasicMaterial({
      vertexColors:true, transparent:true, opacity:0.62 })));

    for (var j=0;j<3;j++){
      var sm=new THREE.Sprite(new THREE.SpriteMaterial({
        map:sprite, color:C_GOLD, transparent:true, opacity:0.95,
        blending:THREE.AdditiveBlending, depthWrite:false }));
      sm.scale.setScalar(0.052);
      world.add(sm);
      movers.push({s:sm, pts:pts, off:(li*0.137+j/3)%1, spd:0.30+((li*7+j)%5)*0.035});
    }
  });

  /* отметки портов */
  var pg=new THREE.BufferGeometry().setFromPoints(ports);
  world.add(new THREE.Points(pg, new THREE.PointsMaterial({
    map:sprite, color:C_GOLD, size:0.075, transparent:true,
    depthWrite:false, sizeAttenuation:true })));

  function layout(){
    var w=cv.clientWidth, h=cv.clientHeight;
    if (!w || !h) return;
    var pr=Math.min(window.devicePixelRatio||1, 1.75);
    renderer.setPixelRatio(pr);
    renderer.setSize(w,h,false);
    dotMat.uniforms.uPR.value = pr;
    camera.aspect=w/h;
    var narrow = w < 940;
    /* канвас квадратный, поэтому отводим камеру ровно настолько, чтобы шар
       вместе с ореолом занимал заданную долю кадра по меньшей стороне */
    var frac = narrow ? 0.90 : 0.94;
    var fit  = Math.min(1, camera.aspect);
    var dist = (R*1.19*2/(frac*fit)) / (2*Math.tan(camera.fov*Math.PI/360));
    camera.position.set(0, 0.30, dist);
    camera.lookAt(0,0,0);
    dotMat.uniforms.uSize.value = narrow ? 5.0 : 7.4;
    camera.updateProjectionMatrix();
  }
  var t0=performance.now();
  function tick(now){
    /* now у rAF это метка начала кадра: в первом кадре она может оказаться
       на доли миллисекунды раньше t0, отсюда отрицательное время. Отсекаем. */
    var t = reduce ? 1.2 : Math.max(0, (now-t0)/1000);
    world.rotation.y = 0.5 + t*0.20;
    dotMat.uniforms.uT.value = t;
    movers.forEach(function(m){
      var last=m.pts.length-1;
      var u=(((t*m.spd)+m.off)%1+1)%1;
      var f=u*last, i=Math.min(last-1, Math.max(0, Math.floor(f)));
      m.s.position.lerpVectors(m.pts[i], m.pts[i+1], f-i);
      var k=Math.sin(Math.PI*u);
      m.s.material.opacity = 0.95*Math.min(1, k*3.2);
      m.s.scale.setScalar(0.030 + 0.034*k);
    });
    renderer.render(scene,camera);
    requestAnimationFrame(tick);
  }
  window.addEventListener('resize', layout, {passive:true});
  layout(); requestAnimationFrame(tick);
})();
});
</script>'''
open("globe.html","w").write(globe)
print("globe.html", len(globe), "байт")
