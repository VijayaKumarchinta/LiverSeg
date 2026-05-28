<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { RotateCcw, ZoomIn, ZoomOut, Maximize2, Move } from 'lucide-vue-next'
import ComparisonSlider from './ComparisonSlider.vue'
import SliceNavigator from './SliceNavigator.vue'

const props = defineProps({
  patient: {
    type: Object,
    default: null
  },
  currentSlice: {
    type: Number,
    required: true
  },
  ww: {
    type: Number,
    default: 400
  },
  wl: {
    type: Number,
    default: 40
  },
  maskOpacity: {
    type: Number,
    default: 65
  },
  showGroundTruth: {
    type: Boolean,
    default: false
  },
  showLesions: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:currentSlice'])

// Canvas Ref
const canvasRef = ref(null)

// Viewer state
const activeMode = ref('overlay') // 'original', 'overlay', 'groundTruth', 'split', 'heatmap'
const zoomScale = ref(1.0)
const panX = ref(0)
const panY = ref(0)
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })

// Animation progress for mask appearing
const maskAnimationProgress = ref(1.0)
let animationFrameId = null

// Split slider percentage
const splitPercent = ref(50)

// Hover HU HUD telemetry
const hoverHU = ref(-1000)
const hoverOrgan = ref('Air')
const mouseX = ref(0)
const mouseY = ref(0)

// Get active slice data
const sliceData = computed(() => {
  if (!props.patient || !props.patient.slices) return null
  return props.patient.slices[props.currentSlice]
})

// Trigger mask tracing animation
const triggerMaskAnimation = () => {
  cancelAnimationFrame(animationFrameId)
  maskAnimationProgress.value = 0
  
  const startTime = performance.now()
  const duration = 750 // ms
  
  const animate = (time) => {
    const elapsed = time - startTime
    const progress = Math.min(elapsed / duration, 1.0)
    
    // Ease out quad
    maskAnimationProgress.value = progress * (2 - progress)
    draw()
    
    if (progress < 1.0) {
      animationFrameId = requestAnimationFrame(animate)
    }
  }
  
  animationFrameId = requestAnimationFrame(animate)
}

// Reset viewer transforms
const resetView = () => {
  zoomScale.value = 1.0
  panX.value = 0
  panY.value = 0
  draw()
}

// Zoom helpers
const zoomIn = () => {
  zoomScale.value = Math.min(5.0, zoomScale.value + 0.15)
  draw()
}

const zoomOut = () => {
  zoomScale.value = Math.max(0.5, zoomScale.value - 0.15)
  draw()
}

// Mouse event handlers for dragging/panning
const onMouseDown = (e) => {
  isDragging.value = true
  dragStart.value = { x: e.clientX - panX.value, y: e.clientY - panY.value }
}

const onMouseMove = (e) => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  const rect = canvas.getBoundingClientRect()
  const currentX = e.clientX - rect.left
  const currentY = e.clientY - rect.top
  
  // Track pan
  if (isDragging.value) {
    panX.value = e.clientX - dragStart.value.x
    panY.value = e.clientY - dragStart.value.y
    draw()
  }
  
  // Calculate un-transformed mouse position for HU calculations
  // Transform sequence: translate(width/2 + panX, height/2 + panY) -> scale(zoomScale) -> translate(-width/2, -height/2)
  const normX = (currentX - rect.width / 2 - panX.value) / zoomScale.value + rect.width / 2
  const normY = (currentY - rect.height / 2 - panY.value) / zoomScale.value + rect.height / 2
  
  calculateHUTelemetry(normX, normY)
}

const onMouseUp = () => {
  isDragging.value = false
}

const onMouseLeave = () => {
  isDragging.value = false
  hoverHU.value = -1000
  hoverOrgan.value = 'Air'
}

const onWheel = (e) => {
  e.preventDefault()
  const zoomFactor = e.deltaY < 0 ? 1.05 : 0.95
  zoomScale.value = Math.max(0.5, Math.min(5.0, zoomScale.value * zoomFactor))
  draw()
}

// Check which region the mouse coordinates belong to
const calculateHUTelemetry = (x, y) => {
  // Center is at 256, 256
  const dx = x - 256
  const dy = y - 256
  
  // Body fat wall ellipse: (x/220)^2 + (y/165)^2 = 1
  const fatDist = (dx * dx) / (220 * 220) + (dy * dy) / (165 * 165)
  // Abdominal cavity ellipse: (x/200)^2 + (y/150)^2 = 1
  const cavityDist = (dx * dx) / (200 * 200) + (dy * dy) / (150 * 150)
  
  if (fatDist > 1.08) {
    // Outside body
    hoverHU.value = -1000
    hoverOrgan.value = 'Air'
    return
  }
  
  // Spine vertebra body: center around 256, 380, radius 35, 25
  const spineDist = ((x - 256) * (x - 256)) / (35 * 35) + ((y - 380) * (y - 380)) / (25 * 25)
  if (spineDist < 1.0) {
    // Spinal canal
    const canalDist = Math.sqrt((x - 256) * (x - 256) + (y - 385) * (y - 385))
    if (canalDist < 8) {
      hoverHU.value = 15 // Cerebrospinal fluid
      hoverOrgan.value = 'Spinal Canal'
    } else {
      hoverHU.value = 750 // Cortical Bone
      hoverOrgan.value = 'Vertebral Bone'
    }
    return
  }
  
  // Left Kidney: (190, 330)
  const lKidneyDist = ((x - 190) * (x - 190)) / (20 * 20) + ((y - 330) * (y - 330)) / (32 * 32)
  if (lKidneyDist < 1.0) {
    hoverHU.value = 45
    hoverOrgan.value = 'Left Kidney'
    return
  }
  
  // Right Kidney: (322, 330)
  const rKidneyDist = ((x - 322) * (x - 322)) / (20 * 20) + ((y - 330) * (y - 330)) / (32 * 32)
  if (rKidneyDist < 1.0) {
    hoverHU.value = 45
    hoverOrgan.value = 'Right Kidney'
    return
  }
  
  // Spleen: (370, 220)
  const spleenDist = ((x - 370) * (x - 370)) / (30 * 30) + ((y - 220) * (y - 220)) / (45 * 45)
  if (spleenDist < 1.0) {
    hoverHU.value = 42
    hoverOrgan.value = 'Spleen'
    return
  }
  
  // Stomach: (300, 160)
  const stomachDist = ((x - 300) * (x - 300)) / (40 * 40) + ((y - 160) * (y - 160)) / (25 * 25)
  if (stomachDist < 1.0) {
    const airDist = Math.sqrt((x - 295) * (x - 295) + (y - 155) * (y - 155))
    if (airDist < 12) {
      hoverHU.value = -950
      hoverOrgan.value = 'Stomach Gas'
    } else {
      hoverHU.value = 10
      hoverOrgan.value = 'Stomach Fluid'
    }
    return
  }

  // Aorta: (244, 345), radius 12
  const aortaDist = Math.sqrt((x - 244) * (x - 244) + (y - 345) * (y - 345))
  if (aortaDist < 12) {
    hoverHU.value = 120 // Contrast enhanced blood
    hoverOrgan.value = 'Abdominal Aorta'
    return
  }

  // Check Liver region
  // In drawing, we translate the liver by 256 + liverX * 2, 256 + liverY * 2
  // and scale by size/50
  if (sliceData.value && sliceData.value.liverSize > 0) {
    const lX = sliceData.value.liverX
    const lY = sliceData.value.liverY
    const size = sliceData.value.liverSize
    
    // Transform coordinates back to the local liver frame
    const lx = (x - (256 + lX * 2)) / (size / 50) + 256
    const ly = (y - (256 + lY * 2)) / (size / 50) + 256
    
    // Liver outline path approximation:
    // MoveTo(110, 200), CubicTo(130, 90, 240, 110, 260, 180), CubicTo(270, 220, 250, 280, 200, 290), CubicTo(150, 300, 90, 260, 110, 200)
    // Distance from centroid:
    const clx = lx - 180
    const cly = ly - 200
    const liverDist = Math.sqrt(clx * clx + cly * cly)
    
    if (liverDist < 75) {
      // Check if mouse is near the lesion
      if (sliceData.value.lesionSize > 0) {
        const lesX = sliceData.value.lesionX * 2 - 30
        const lesY = sliceData.value.lesionY * 2 + 10
        const lesR = sliceData.value.lesionSize * 40
        const mouseLesionDist = Math.sqrt((x - 256 - lesX) * (x - 256 - lesX) + (y - 256 - lesY) * (y - 256 - lesY))
        if (mouseLesionDist < lesR) {
          hoverHU.value = 25 // Hypodense lesion
          hoverOrgan.value = 'Focal Hepatic Lesion'
          return
        }
      }
      
      hoverHU.value = 58
      hoverOrgan.value = 'Liver Parenchyma'
      return
    }
  }
  
  if (cavityDist < 1.0) {
    // general cavity soft tissue/fluid
    hoverHU.value = 8
    hoverOrgan.value = 'Peritoneal Cavity'
  } else {
    // Fat layer
    hoverHU.value = -90
    hoverOrgan.value = 'Subcutaneous Fat'
  }
}

// High-fidelity procedural CT noise pattern
let noiseCanvas = null

const initNoise = () => {
  noiseCanvas = document.createElement('canvas')
  noiseCanvas.width = 128
  noiseCanvas.height = 128
  const nCtx = noiseCanvas.getContext('2d')
  const imgData = nCtx.createImageData(128, 128)
  const data = imgData.data
  for (let i = 0; i < data.length; i += 4) {
    // Generate fine-grained quantum mottle noise (centered around 128)
    const val = 128 + (Math.random() - 0.5) * 55
    data[i] = val
    data[i+1] = val
    data[i+2] = val
    data[i+3] = 255
  }
  nCtx.putImageData(imgData, 0, 0)
}

// Detailed anatomical drawing routines
const drawSpine = (ctx) => {
  ctx.save()
  
  // 1. Posterior Back Muscle Groups (Erector spinae)
  ctx.fillStyle = '#111113'
  ctx.strokeStyle = '#222225'
  ctx.lineWidth = 1
  
  // Left side muscles
  ctx.beginPath()
  ctx.ellipse(215, 395, 26, 20, -Math.PI / 10, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // Right side muscles
  ctx.beginPath()
  ctx.ellipse(297, 395, 26, 20, Math.PI / 10, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // Muscle fiber texture lines
  ctx.strokeStyle = '#18181b'
  ctx.lineWidth = 0.5
  for (let r = 5; r <= 20; r += 5) {
    ctx.beginPath()
    ctx.ellipse(215, 395, r, r * 0.75, -Math.PI / 10, 0, Math.PI * 2)
    ctx.stroke()
    ctx.beginPath()
    ctx.ellipse(297, 395, r, r * 0.75, Math.PI / 10, 0, Math.PI * 2)
    ctx.stroke()
  }
  
  // 2. Psoas Major Muscles (deep anterior-lateral to spine)
  ctx.fillStyle = '#151518'
  ctx.beginPath()
  ctx.ellipse(216, 348, 17, 13, Math.PI / 8, 0, Math.PI * 2)
  ctx.ellipse(296, 348, 17, 13, -Math.PI / 8, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()

  // 3. Vertebral Body Cortical Bone (Bright bone cortex)
  ctx.fillStyle = '#e2e8f0'
  ctx.strokeStyle = '#94a3b8'
  ctx.lineWidth = 1.2
  
  // Anatomical kidney/heart shape of lumbar vertebra body
  ctx.beginPath()
  ctx.moveTo(226, 368)
  ctx.bezierCurveTo(240, 361, 272, 361, 286, 368)
  ctx.bezierCurveTo(294, 375, 290, 390, 278, 394)
  ctx.bezierCurveTo(266, 398, 246, 398, 234, 394)
  ctx.bezierCurveTo(222, 390, 218, 375, 226, 368)
  ctx.closePath()
  ctx.fill()
  ctx.stroke()
  
  // Vertebral Body Medulla (Bone marrow - grey density)
  ctx.fillStyle = '#475569'
  ctx.beginPath()
  ctx.moveTo(230, 372)
  ctx.bezierCurveTo(242, 366, 270, 366, 282, 372)
  ctx.bezierCurveTo(286, 377, 283, 386, 274, 389)
  ctx.bezierCurveTo(264, 392, 248, 392, 238, 389)
  ctx.bezierCurveTo(228, 386, 225, 377, 230, 372)
  ctx.closePath()
  ctx.fill()
  
  // 4. Neural Arch (Pedicles, Laminas, processes surrounding spinal canal)
  ctx.fillStyle = '#e2e8f0'
  // Left/Right Pedicles
  ctx.beginPath()
  ctx.moveTo(232, 392); ctx.lineTo(224, 408); ctx.lineTo(234, 408); ctx.lineTo(240, 394); ctx.closePath()
  ctx.moveTo(280, 392); ctx.lineTo(288, 408); ctx.lineTo(278, 408); ctx.lineTo(272, 394); ctx.closePath()
  // Spinous process and laminae
  ctx.moveTo(224, 408)
  ctx.lineTo(248, 418)
  ctx.lineTo(256, 440) // spinous process tip
  ctx.lineTo(264, 418)
  ctx.lineTo(288, 408)
  ctx.lineTo(280, 416)
  ctx.lineTo(256, 425)
  ctx.lineTo(232, 416)
  ctx.closePath()
  
  // Left Transverse Process
  ctx.moveTo(226, 394); ctx.lineTo(202, 397); ctx.lineTo(200, 402); ctx.lineTo(224, 400); ctx.closePath()
  // Right Transverse Process
  ctx.moveTo(286, 394); ctx.lineTo(310, 397); ctx.lineTo(312, 402); ctx.lineTo(288, 400); ctx.closePath()
  ctx.fill()
  ctx.stroke()
  
  // 5. Spinal Canal (CSF filled space, dark)
  ctx.fillStyle = '#000000'
  ctx.beginPath()
  ctx.ellipse(256, 402, 11, 8.5, 0, 0, Math.PI * 2)
  ctx.fill()
  
  // 6. Spinal Cord (nervous tissue, grey)
  ctx.fillStyle = '#64748b'
  ctx.beginPath()
  ctx.ellipse(256, 402, 5, 4, 0, 0, Math.PI * 2)
  ctx.fill()
  
  ctx.restore()
}

const drawRib = (ctx, rx, ry, rotation) => {
  ctx.save()
  ctx.translate(rx, ry)
  ctx.rotate(rotation)
  
  // Cortical outer bone (highly dense, white)
  ctx.fillStyle = '#f8fafc'
  ctx.strokeStyle = '#94a3b8'
  ctx.lineWidth = 1.0
  ctx.beginPath()
  ctx.ellipse(0, 0, 15, 6, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // Medullary bone center (spongey bone marrow, dark grey)
  ctx.fillStyle = '#27272a'
  ctx.beginPath()
  ctx.ellipse(0, 0, 11.5, 3.5, 0, 0, Math.PI * 2)
  ctx.fill()
  
  ctx.restore()
}

const drawBowelLoopsSoft = (ctx) => {
  ctx.save()
  const drawLoop = (bx, by, w, h, rot, fill) => {
    ctx.save()
    ctx.translate(bx, by)
    ctx.rotate(rot)
    ctx.fillStyle = fill
    ctx.beginPath()
    ctx.ellipse(0, 0, w, h, 0, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()
  }
  
  // Soft tissue borders/walls of bowel loops
  drawLoop(295, 215, 14, 9, Math.PI / 4, '#121215')
  drawLoop(330, 200, 19, 12, -Math.PI / 6, '#141417')
  drawLoop(315, 245, 13, 10, Math.PI / 12, '#141416')
  drawLoop(345, 235, 11, 7, -Math.PI / 3, '#101012')
  drawLoop(355, 175, 17, 13, Math.PI / 3, '#161619')
  
  ctx.restore()
}

const drawLiverVessels = (ctx, lX, lY, size) => {
  ctx.save()
  ctx.translate(256 + lX * 2, 256 + lY * 2)
  ctx.scale(size / 50, size / 50)
  ctx.translate(-256, -256)
  
  // Portal and hepatic veins (hypodense lines/branching structures in tissue)
  ctx.strokeStyle = '#414147' // soft contrast blending inside liver
  ctx.lineWidth = 2.0
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  
  // Right hepatic branches
  ctx.beginPath()
  ctx.moveTo(190, 235) // Hilum region
  ctx.quadraticCurveTo(158, 215, 136, 222)
  ctx.moveTo(158, 215)
  ctx.quadraticCurveTo(142, 195, 124, 201)
  ctx.moveTo(144, 218)
  ctx.quadraticCurveTo(128, 232, 115, 226)
  ctx.stroke()
  
  // Middle hepatic branches
  ctx.lineWidth = 1.4
  ctx.beginPath()
  ctx.moveTo(190, 235)
  ctx.quadraticCurveTo(182, 195, 172, 172)
  ctx.moveTo(180, 190)
  ctx.quadraticCurveTo(192, 170, 202, 155)
  ctx.stroke()
  
  // Left hepatic branches
  ctx.lineWidth = 1.0
  ctx.beginPath()
  ctx.moveTo(190, 235)
  ctx.quadraticCurveTo(215, 215, 235, 210)
  ctx.stroke()
  
  ctx.restore()
}

const drawLiverShape = (ctx, fillColor, strokeColor, strokeWidth) => {
  if (!sliceData.value || sliceData.value.liverSize <= 0) return
  const lX = sliceData.value.liverX
  const lY = sliceData.value.liverY
  const size = sliceData.value.liverSize
  
  ctx.save()
  ctx.translate(256 + lX * 2, 256 + lY * 2)
  ctx.scale(size / 50, size / 50)
  ctx.translate(-256, -256)
  
  ctx.beginPath()
  // Medically realistic liver contour (triangular lobe, lateral dome, portal notch)
  ctx.moveTo(110, 190)
  ctx.bezierCurveTo(125, 95, 235, 115, 260, 185)
  ctx.bezierCurveTo(270, 215, 265, 260, 245, 275)
  ctx.bezierCurveTo(230, 285, 205, 265, 195, 250) // Porta hepatis notch
  ctx.bezierCurveTo(185, 260, 175, 285, 155, 290)
  ctx.bezierCurveTo(125, 295, 95, 245, 110, 190)
  ctx.closePath()
  
  if (fillColor) {
    ctx.fillStyle = fillColor
    ctx.fill()
  }
  if (strokeColor && strokeWidth > 0) {
    ctx.strokeStyle = strokeColor
    ctx.lineWidth = strokeWidth
    ctx.stroke()
  }
  
  ctx.restore()
}

// Procedural Abdominal CT Slice Drawing routine
const draw = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  
  const width = canvas.width
  const height = canvas.height
  
  // Clear background
  ctx.fillStyle = '#000000'
  ctx.fillRect(0, 0, width, height)
  
  // 1. Draw Ring Reconstruction Artifacts (faint circles in vacuum scanner)
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.007)'
  ctx.lineWidth = 5
  ctx.beginPath()
  ctx.arc(width/2, height/2, 125, 0, Math.PI*2)
  ctx.stroke()
  ctx.beginPath()
  ctx.arc(width/2, height/2, 215, 0, Math.PI*2)
  ctx.stroke()

  // 2. Draw Patient Gantry Couch (CT Scanner table at bottom)
  ctx.save()
  // Crescent support table arc
  ctx.strokeStyle = '#18181c'
  ctx.lineWidth = 3
  ctx.beginPath()
  ctx.arc(256, 170, 310, 0.38 * Math.PI, 0.62 * Math.PI)
  ctx.stroke()
  
  ctx.strokeStyle = '#0e0e11'
  ctx.lineWidth = 1.5
  ctx.beginPath()
  ctx.arc(256, 177, 310, 0.39 * Math.PI, 0.61 * Math.PI)
  ctx.stroke()
  
  // Flat couch slider base
  ctx.fillStyle = '#070709'
  ctx.beginPath()
  ctx.moveTo(140, 465)
  ctx.lineTo(372, 465)
  ctx.lineTo(320, 488)
  ctx.lineTo(192, 488)
  ctx.closePath()
  ctx.fill()
  ctx.strokeStyle = '#18181c'
  ctx.stroke()
  ctx.restore()

  // Save transform state for patient abdominal volume positioning
  ctx.save()
  
  // Apply Zoom & Pan transforms around canvas center
  ctx.translate(width / 2 + panX.value, height / 2 + panY.value)
  ctx.scale(zoomScale.value, zoomScale.value)
  ctx.translate(-width / 2, -height / 2)
  
  // --- LAYER 1: SOFT TISSUES (with clinical Gaussian blur) ---
  ctx.save()
  ctx.filter = 'blur(2.2px)'
  
  // Subcutaneous Fat layer (outer anatomical contour, hypodense/dark gray)
  ctx.fillStyle = '#0f0f11'
  ctx.beginPath()
  ctx.ellipse(256, 256, 226, 169, 0, 0, Math.PI * 2)
  ctx.fill()
  
  // Subcutaneous fibrous septae (lines in fat layer)
  ctx.strokeStyle = 'rgba(75, 85, 99, 0.12)'
  ctx.lineWidth = 0.8
  for (let angle = 0; angle < Math.PI * 2; angle += 0.25) {
    const x1 = 256 + Math.cos(angle) * 211
    const y1 = 256 + Math.sin(angle) * 156
    const x2 = 256 + Math.cos(angle) * 221
    const y2 = 256 + Math.sin(angle) * 164
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.quadraticCurveTo((x1+x2)/2 + (Math.random()-0.5)*4, (y1+y2)/2 + (Math.random()-0.5)*4, x2, y2)
    ctx.stroke()
  }

  // Abdominal Cavity Wall (deep peritoneal cavity, muscle band)
  ctx.strokeStyle = '#1b1b1e'
  ctx.lineWidth = 7.0
  ctx.beginPath()
  ctx.ellipse(256, 256, 204, 148, 0, 0, Math.PI * 2)
  ctx.stroke()
  
  ctx.fillStyle = '#050507'
  ctx.beginPath()
  ctx.ellipse(256, 256, 200, 144, 0, 0, Math.PI * 2)
  ctx.fill()
  
  // Back muscles (erector spinae)
  ctx.fillStyle = '#141417'
  ctx.beginPath()
  ctx.ellipse(215, 395, 26, 20, -Math.PI / 10, 0, Math.PI * 2)
  ctx.ellipse(297, 395, 26, 20, Math.PI / 10, 0, Math.PI * 2)
  ctx.fill()
  
  // Psoas major muscles
  ctx.fillStyle = '#18181b'
  ctx.beginPath()
  ctx.ellipse(216, 348, 17, 13, Math.PI / 8, 0, Math.PI * 2)
  ctx.ellipse(296, 348, 17, 13, -Math.PI / 8, 0, Math.PI * 2)
  ctx.fill()
  
  // Kidneys
  ctx.fillStyle = '#222226'
  ctx.beginPath()
  ctx.ellipse(190, 330, 20, 32, -Math.PI / 8, 0, Math.PI * 2)
  ctx.ellipse(322, 330, 20, 32, Math.PI / 8, 0, Math.PI * 2)
  ctx.fill()
  
  // Spleen
  ctx.fillStyle = '#27272b'
  ctx.beginPath()
  ctx.ellipse(370, 220, 32, 48, Math.PI / 5, 0, Math.PI * 2)
  ctx.fill()
  
  // Stomach (fluid filled space)
  ctx.fillStyle = '#141417'
  ctx.beginPath()
  ctx.ellipse(300, 160, 42, 28, -Math.PI / 10, 0, Math.PI * 2)
  ctx.fill()
  
  // Bowel loops
  drawBowelLoopsSoft(ctx)
  
  // Liver tissue parenchyma
  drawLiverShape(ctx, '#2c2c31', null, 0)
  
  // Branching portal venous structures (softly blended)
  if (sliceData.value && sliceData.value.liverSize > 0) {
    drawLiverVessels(ctx, sliceData.value.liverX, sliceData.value.liverY, sliceData.value.liverSize)
  }
  
  // Focal lesion necrotic center (soft hypodense center)
  if (sliceData.value && sliceData.value.lesionSize > 0) {
    const lesX = sliceData.value.lesionX * 2 - 30
    const lesY = sliceData.value.lesionY * 2 + 10
    const lesSize = sliceData.value.lesionSize
    ctx.beginPath()
    ctx.arc(lesX, lesY, lesSize * 36, 0, Math.PI * 2)
    ctx.fillStyle = '#161619'
    ctx.fill()
  }
  
  ctx.restore()
  
  // --- LAYER 2: SHARP ELEMENTS (Bones, borders, gas, contrast, annotations) ---
  ctx.save()
  ctx.filter = 'blur(0.2px)'
  
  // Outer Skin border (very thin line)
  ctx.strokeStyle = '#3e3e44'
  ctx.lineWidth = 0.8
  ctx.beginPath()
  ctx.ellipse(256, 256, 227.5, 170.5, 0, 0, Math.PI * 2)
  ctx.stroke()
  
  // Ribs
  drawRib(ctx, 72, 190, -Math.PI / 6)
  drawRib(ctx, 60, 250, 0)
  drawRib(ctx, 72, 310, Math.PI / 6)
  drawRib(ctx, 440, 190, Math.PI / 6)
  drawRib(ctx, 452, 250, 0)
  drawRib(ctx, 440, 310, -Math.PI / 6)
  
  // Spine
  drawSpine(ctx)
  
  // Aorta (contrast enhanced)
  ctx.fillStyle = '#ffffff'
  ctx.strokeStyle = '#4b5563'
  ctx.lineWidth = 1.0
  ctx.beginPath()
  ctx.arc(244, 345, 11, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // Vena Cava (flat contrast-enhanced oval)
  ctx.fillStyle = '#cbd5e1'
  ctx.strokeStyle = '#374151'
  ctx.beginPath()
  ctx.ellipse(268, 345, 12, 8, Math.PI / 6, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // Stomach and Bowel Gas pockets (pure black)
  ctx.fillStyle = '#000000'
  ctx.beginPath()
  ctx.arc(292, 154, 13, 0, Math.PI * 2) // stomach gas
  ctx.ellipse(330, 200, 19, 12, -Math.PI / 6, 0, Math.PI * 2) // bowel gas
  ctx.fill()
  
  // Oral contrast inside bowel (bright white spots)
  ctx.fillStyle = '#ffffff'
  ctx.beginPath()
  ctx.arc(313, 243, 3, 0, Math.PI * 2)
  ctx.arc(320, 247, 2.5, 0, Math.PI * 2)
  ctx.fill()
  
  // Liver border (thin grey boundary)
  drawLiverShape(ctx, null, '#414147', 1.0)
  
  // Render modes on top
  if (activeMode.value === 'overlay') {
    // Overlay semi-transparent AI segmentation mask (teal)
    const alpha = (props.maskOpacity / 100) * maskAnimationProgress.value
    drawLiverShape(ctx, `rgba(20, 184, 166, ${alpha})`, '#14b8a6', alpha > 0 ? 1.2 : 0)
    
    // Draw focal lesion AI contour
    if (sliceData.value && sliceData.value.lesionSize > 0) {
      drawLesionInternal(ctx, props.showLesions)
    }
  } else if (activeMode.value === 'heatmap') {
    // Draw confidence radial gradient heatmap
    drawHeatmapInternal(ctx)
    
    // Draw focal lesion AI contour
    if (sliceData.value && sliceData.value.lesionSize > 0) {
      drawLesionInternal(ctx, props.showLesions)
    }
  } else if (activeMode.value === 'groundTruth') {
    // Draw AI Mask (teal)
    const alpha = (props.maskOpacity / 100) * maskAnimationProgress.value
    drawLiverShape(ctx, `rgba(20, 184, 166, ${alpha})`, '#14b8a6', alpha > 0 ? 1.2 : 0)
    
    // Draw Ground Truth contour (dashed green)
    if (props.showGroundTruth) {
      ctx.save()
      ctx.setLineDash([4, 4])
      // Shift slightly for visual comparison
      if (sliceData.value && sliceData.value.liverSize > 0) {
        const lX = sliceData.value.liverX + 1.2
        const lY = sliceData.value.liverY - 0.8
        const size = sliceData.value.liverSize
        
        ctx.translate(256 + lX * 2, 256 + lY * 2)
        ctx.scale(size / 50, size / 50)
        ctx.translate(-256, -256)
        
        ctx.beginPath()
        ctx.moveTo(110, 190)
        ctx.bezierCurveTo(125, 95, 235, 115, 260, 185)
        ctx.bezierCurveTo(270, 215, 265, 260, 245, 275)
        ctx.bezierCurveTo(230, 285, 205, 265, 195, 250)
        ctx.bezierCurveTo(185, 260, 175, 285, 155, 290)
        ctx.bezierCurveTo(125, 295, 95, 245, 110, 190)
        ctx.closePath()
        
        ctx.strokeStyle = '#10b981'
        ctx.lineWidth = 1.5
        ctx.stroke()
      }
      ctx.restore()
    }
    
    // Draw lesion
    if (sliceData.value && sliceData.value.lesionSize > 0) {
      drawLesionInternal(ctx, props.showLesions)
    }
  } else if (activeMode.value === 'split') {
    // Draggable split clip screen dividing original scan vs segmentation overlay
    const splitX = width * (splitPercent.value / 100)
    
    // We clip drawing so right of splitPercent shows the AI mask
    ctx.save()
    ctx.beginPath()
    ctx.rect(splitX, 0, width - splitX, height)
    ctx.clip()
    
    const alpha = props.maskOpacity / 100
    drawLiverShape(ctx, `rgba(20, 184, 166, ${alpha})`, '#14b8a6', 1.2)
    if (sliceData.value && sliceData.value.lesionSize > 0) {
      drawLesionInternal(ctx, props.showLesions)
    }
    ctx.restore()
  }
  
  ctx.restore() // Restore sharp transform
  ctx.restore() // Restore abdominal scale transforms
  
  // 13. Draw Quantum Mottle Noise overlay on the complete canvas
  if (noiseCanvas) {
    ctx.save()
    ctx.globalCompositeOperation = 'overlay'
    ctx.globalAlpha = 0.16 // Realistic speckle noise level
    const pattern = ctx.createPattern(noiseCanvas, 'repeat')
    ctx.fillStyle = pattern
    ctx.fillRect(0, 0, width, height)
    ctx.restore()
  }
}

// Inner helper to draw necrotic focal lesions
const drawLesionInternal = (ctx, highlighted) => {
  if (!sliceData.value || sliceData.value.lesionSize <= 0) return
  const lesX = sliceData.value.lesionX * 2 - 30
  const lesY = sliceData.value.lesionY * 2 + 10
  const lesSize = sliceData.value.lesionSize
  
  ctx.save()
  ctx.translate(256, 256)
  
  // Necrotic necrotic center (hypodense tumor tissue)
  ctx.beginPath()
  ctx.arc(lesX, lesY, lesSize * 36, 0, Math.PI * 2)
  ctx.fillStyle = '#1c1c1f'
  ctx.fill()
  
  if (highlighted) {
    // Red AI contour outline
    ctx.strokeStyle = '#ef4444'
    ctx.lineWidth = 1.2
    ctx.stroke()
    
    // Transparent red fill
    ctx.fillStyle = 'rgba(239, 68, 68, 0.28)'
    ctx.fill()
  } else {
    // Unhighlighted lesion tissue border
    ctx.strokeStyle = '#2d2d34'
    ctx.lineWidth = 0.8
    ctx.stroke()
  }
  ctx.restore()
}

// Inner helper to draw confidence heatmap
const drawHeatmapInternal = (ctx) => {
  if (!sliceData.value || sliceData.value.liverSize <= 0) return
  const lX = sliceData.value.liverX
  const lY = sliceData.value.liverY
  const size = sliceData.value.liverSize
  
  ctx.save()
  ctx.translate(256 + lX * 2, 256 + lY * 2)
  ctx.scale(size / 50, size / 50)
  ctx.translate(-256, -256)
  
  ctx.beginPath()
  ctx.moveTo(110, 190)
  ctx.bezierCurveTo(125, 95, 235, 115, 260, 185)
  ctx.bezierCurveTo(270, 215, 265, 260, 245, 275)
  ctx.bezierCurveTo(230, 285, 205, 265, 195, 250)
  ctx.bezierCurveTo(185, 260, 175, 285, 155, 290)
  ctx.bezierCurveTo(125, 295, 95, 245, 110, 190)
  ctx.closePath()
  ctx.clip()
  
  // Radial heatmap centered around hilum/lesion area
  const grad = ctx.createRadialGradient(180, 200, 5, 180, 200, 80)
  grad.addColorStop(0, 'rgba(239, 68, 68, 0.82)')   // Hottest likelihood (focal tumor)
  grad.addColorStop(0.35, 'rgba(234, 179, 8, 0.65)') // High likelihood
  grad.addColorStop(0.75, 'rgba(20, 184, 166, 0.42)') // Normal parenchyma border
  grad.addColorStop(1, 'rgba(20, 184, 166, 0.12)')
  
  ctx.fillStyle = grad
  ctx.fill()
  
  ctx.strokeStyle = '#14b8a6'
  ctx.lineWidth = 1.5
  ctx.stroke()
  
  ctx.restore()
}

// Watchers to trigger redrawing when sliders, props, or slices update
watch(() => [props.currentSlice, props.ww, props.wl, props.maskOpacity, props.showGroundTruth, props.showLesions], () => {
  draw()
})

// Trigger animation on mount or when mode changes to overlay
watch(activeMode, (newMode) => {
  if (newMode === 'overlay' || newMode === 'groundTruth') {
    triggerMaskAnimation()
  } else {
    draw()
  }
})

// CSS contrast filter mapping from WW and WL aligning with clinical Hounsfield logic
const ctFilterStyle = computed(() => {
  const contrast = (400 / props.ww).toFixed(2)
  const brightness = ((180 - props.wl) / 140).toFixed(2)
  return {
    filter: `contrast(${contrast}) brightness(${brightness})`
  }
})

// Event listener setup
onMounted(() => {
  initNoise()
  draw()
  triggerMaskAnimation()
  
  // Add global mouse up listener to finalize drag safely
  window.addEventListener('mouseup', onMouseUp)
})

onUnmounted(() => {
  window.removeEventListener('mouseup', onMouseUp)
  cancelAnimationFrame(animationFrameId)
})
</script>

<template>
  <div class="frosted-glass-panel p-4 flex flex-col justify-between min-h-[500px] bg-slate-900 text-white relative">
    
    <!-- Viewer Header / PACS HUD Bar -->
    <div class="flex items-center justify-between pb-3.5 border-b border-slate-800">
      <div class="text-[9px] font-mono text-slate-400 space-y-0.5 font-semibold">
        <div>ACTIVE CASE: {{ patient?.id || 'NO_CASE' }}</div>
        <div>RESOLUTION: 512 x 512 x 20 voxels &middot; Slice {{ currentSlice + 1 }} of 20</div>
      </div>
      
      <!-- Toolbar Controls -->
      <div class="flex items-center gap-2">
        <button 
          @click="zoomIn"
          class="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
          title="Zoom In"
        >
          <ZoomIn class="w-3.5 h-3.5" />
        </button>
        <button 
          @click="zoomOut"
          class="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
          title="Zoom Out"
        >
          <ZoomOut class="w-3.5 h-3.5" />
        </button>
        <button 
          @click="resetView"
          class="flex items-center gap-1 text-[9px] font-bold rounded bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 transition-colors"
          title="Reset View Transforms"
        >
          <RotateCcw class="w-3 h-3" /> Reset View
        </button>
      </div>
    </div>

    <!-- Interactive PACS Canvas Viewer -->
    <div class="flex-1 flex items-center justify-center bg-black rounded-xl border border-slate-800 my-4 relative overflow-hidden select-none min-h-[340px]">
      
      <!-- Grayscale Grid Background -->
      <div class="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.012)_1px,transparent_1px)] bg-[size:16px_16px] pointer-events-none"></div>

      <!-- PACS HUD: Patient Demographics overlay -->
      <div class="absolute top-3.5 left-4 text-[9px] font-mono text-slate-400 space-y-0.5 leading-normal pointer-events-none z-10">
        <div class="font-bold text-slate-200">{{ patient?.name || 'Anonymous Patient' }}</div>
        <div>MRN: {{ patient?.id || 'PT-XXXX-K' }}</div>
        <div>Age/Sex: {{ patient?.age }}y / {{ patient?.gender }}</div>
      </div>

      <div class="absolute top-3.5 right-4 text-[9px] font-mono text-slate-400 text-right space-y-0.5 leading-normal pointer-events-none z-10">
        <div class="font-bold text-teal-400">LiversegAI v1.4</div>
        <div>kVp: 120 &middot; mAs: 250</div>
        <div>Thk: 1.0 mm</div>
      </div>

      <!-- Live HU Telemetry Hover Indicator -->
      <div class="absolute bottom-3.5 left-4 text-[9px] font-mono text-slate-400 space-y-0.5 leading-normal pointer-events-none z-10">
        <div class="font-bold text-teal-500">VOXEL PROBE</div>
        <div>Organ: <span class="text-white">{{ hoverOrgan }}</span></div>
        <div>Value: <span class="text-white font-bold">{{ hoverHU }} HU</span></div>
      </div>

      <!-- Navigation & Mode Indicator -->
      <div class="absolute bottom-3.5 right-4 text-[9px] font-mono text-slate-400 text-right space-y-0.5 leading-normal pointer-events-none z-10">
        <div>WW: {{ ww }} HU &middot; WL: {{ wl }} HU</div>
        <div>Zoom: {{ zoomScale.toFixed(2) }}x</div>
        <div>Pos: ({{ panX }}, {{ panY }}) px</div>
      </div>

      <!-- Direction labels (A, P, R, L) -->
      <div class="absolute top-3.5 left-1/2 -translate-x-1/2 text-[10px] font-bold font-mono text-slate-600 pointer-events-none z-10">A</div>
      <div class="absolute bottom-3.5 left-1/2 -translate-x-1/2 text-[10px] font-bold font-mono text-slate-600 pointer-events-none z-10">P</div>
      <div class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[10px] font-bold font-mono text-slate-600 pointer-events-none z-10">R</div>
      <div class="absolute right-3.5 top-1/2 -translate-y-1/2 text-[10px] font-bold font-mono text-slate-600 pointer-events-none z-10">L</div>

      <!-- Grab handle icon indicator on canvas center when panned -->
      <div 
        v-if="zoomScale > 1.05 || Math.abs(panX) > 5 || Math.abs(panY) > 5" 
        class="absolute bottom-3.5 left-1/2 -translate-x-1/2 text-[9px] font-mono text-slate-500 bg-black/60 px-2 py-0.5 rounded flex items-center gap-1 pointer-events-none"
      >
        <Move class="w-3 h-3" /> Panned/Zoomed (Double-click to reset)
      </div>

      <!-- The Core CT Grayscale Canvas -->
      <canvas 
        ref="canvasRef"
        width="512"
        height="512"
        class="w-[320px] h-[320px] md:w-[380px] md:h-[380px] cursor-grab active:cursor-grabbing transition-shadow"
        :style="ctFilterStyle"
        @mousedown="onMouseDown"
        @mousemove="onMouseMove"
        @wheel="onWheel"
        @dblclick="resetView"
      ></canvas>

      <!-- Draggable Split Comparison Slider Overlay -->
      <ComparisonSlider 
        v-if="activeMode === 'split'" 
        v-model="splitPercent"
      />
    </div>

    <!-- Mode Selector Toolbar -->
    <div class="grid grid-cols-5 gap-1.5 p-1 bg-slate-950 border border-slate-800 rounded-xl mb-4 text-[10px]">
      <button 
        @click="activeMode = 'original'"
        :class="[
          'py-1.5 font-bold uppercase rounded-lg text-center transition-colors',
          activeMode === 'original' 
            ? 'bg-slate-800 text-white shadow-sm border border-slate-700/50' 
            : 'text-slate-400 hover:text-slate-200'
        ]"
      >
        Original Scan
      </button>
      <button 
        @click="activeMode = 'overlay'"
        :class="[
          'py-1.5 font-bold uppercase rounded-lg text-center transition-colors',
          activeMode === 'overlay' 
            ? 'bg-teal-500/20 text-teal-350 border border-teal-500/30' 
            : 'text-slate-400 hover:text-slate-200'
        ]"
      >
        AI Mask
      </button>
      <button 
        @click="activeMode = 'groundTruth'"
        :class="[
          'py-1.5 font-bold uppercase rounded-lg text-center transition-colors',
          activeMode === 'groundTruth' 
            ? 'bg-emerald-500/20 text-emerald-350 border border-emerald-500/30' 
            : 'text-slate-400 hover:text-slate-200'
        ]"
      >
        Ground Truth
      </button>
      <button 
        @click="activeMode = 'split'"
        :class="[
          'py-1.5 font-bold uppercase rounded-lg text-center transition-colors',
          activeMode === 'split' 
            ? 'bg-sky-500/20 text-sky-350 border border-sky-500/30' 
            : 'text-slate-400 hover:text-slate-200'
        ]"
      >
        Split Slider
      </button>
      <button 
        @click="activeMode = 'heatmap'"
        :class="[
          'py-1.5 font-bold uppercase rounded-lg text-center transition-colors',
          activeMode === 'heatmap' 
            ? 'bg-amber-500/20 text-amber-350 border border-amber-500/30' 
            : 'text-slate-400 hover:text-slate-200'
        ]"
      >
        Confidence Heatmap
      </button>
    </div>

    <!-- Slice Navigator integration -->
    <SliceNavigator 
      :modelValue="currentSlice"
      @update:modelValue="emit('update:currentSlice', $event)"
      :max="20"
    />
  </div>
</template>
