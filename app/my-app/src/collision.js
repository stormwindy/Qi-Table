
//adapted from https://hackmd.io/@US4ofdv7Sq2GRdxti381_A/ryFmIZrsl?type=view

/**
 * Checks if two shapes overlap and returns a vector that will move them away ([0,0] if no overlap)
 * @param {Object[]} pos1 - geometric center of the first shape
 * @param {Object[]} pos2 - geometric center of the second shape
 * @param {Object[]} vertices1 - the vertices of the first shape
 * @param {Object[]} vertices2 - the vertices of the second shape
 */

export function resolveCollision(pos1, pos2, vertices1, vertices2){
    //get all edges
    let edges = getEdges(vertices1).concat(getEdges(vertices2));
    //get orthogonals of edges
    let orthogonals = edges.map(({x, y}) => {return {x: -y, y: x}});

    let foundSeparation = false;
    let pushVectors = [];
    orthogonals.forEach(o => {
        if (foundSeparation === true) return;
        let min1 = Number.MAX_VALUE;
        let max1 = -Number.MAX_VALUE;
        let min2 = Number.MAX_VALUE;
        let max2 = -Number.MAX_VALUE;
        
        vertices1.forEach(v => {
            let projection = dot(v, o);
            console.log("Projection of [" + v.x +", "+ v.y + "] onto [" + o.x + ", " + o.y + "] equals " + projection);
            min1 = Math.min(min1, projection);
            max1 = Math.max(max1, projection);
        });

        vertices2.forEach(v => {
            let projection = dot(v, o);
            console.log("Projection of [" + v.x +", "+ v.y + "] onto [" + o.x + ", " + o.y + "] equals " + projection);
            min2 = Math.min(min2, projection);
            max2 = Math.max(max2, projection);
        });

        if (max1 >= min2 && max2 >= min1){
            let d = Math.min(max2 - min1, max1 - min2);
            console.log(d);
            d = d/dot(o,o);
            console.log(d);
            pushVectors.push({x: o.x*d, y: o.y*d});
            //pushVectors.push({x: 0, y: 0});
        }
        else {
            console.log("Found separation! o: [" + o.x + ", " + o.y + "]");
            foundSeparation = true;
        }
    });

    if (foundSeparation===true) return {x:0, y:0};
    //find minimum push vector
    let mpv = {x: Infinity, y: Infinity};
    console.log(pushVectors);
    pushVectors.forEach(v => {
        if (dot(v,v)<dot(mpv, mpv)) mpv=v;
    });

    //make sure directions are right
    //direction from 1 to 2
    let dir12 = {x: pos2.x-pos1.x, y: pos2.y-pos1.y};
    if (dot(dir12, mpv)>0) mpv={x: -mpv.x, y: -mpv.y};

    return mpv;
}


/**
 * Gets the counterclockwise vertices of a rectangle defined by konva.js attributes
 * @param {number} x - x axis position of rect's center
 * @param {number} y - y axis position of rect's center
 * @param {number} width - rectangle's width
 * @param {number} height - rectangle's height
 * @param {number} rotation - rectangle's rotation (in degrees)
 */
export function getVertices(x, y, width, height, rotation){
    //distance from center to vertex
    const d = Math.sqrt(Math.pow(width/2, 2)+Math.pow(height/2, 2))
    let vertices = [];
    //FIX ANGLE RECALCULATION
    let angle = Math.atan(width/height);
    const rotationInRad = rotation*Math.PI/180;
    const angles = [2*Math.PI-angle+rotationInRad, Math.PI+angle+rotationInRad,
                     Math.PI-angle+rotationInRad, angle+rotationInRad];
    //console.log(angle);
    //console.log(angles);
    /*
    for (let i=3; i>=0; i-=1){
        let trueAngle = angle+rotationInRad;
        let xDisplacement = d*Math.sin(trueAngle);
        let yDisplacement = d*Math.cos(trueAngle);
        vertices[i] = ({x: x+xDisplacement, y: y+yDisplacement});
        angle+=2*(Math.PI/2-rotationInRad);
    }
    */

    return angles.map((a) => {
        return {x: x+d*Math.sin(a), y: y-d*Math.cos(a)}
    });
}
/**
 * Gets an array of the edge vectors of a shape
 * @param {*} vertices  - the counterclockwise vertices of the shape
 */
export function getEdges(vertices){
    let edges = [];
    
    for (let i=0; i<vertices.length; i++){
        edges.push({
            x: vertices[(i+1)%vertices.length].x - vertices[i].x,
            y: vertices[(i+1)%vertices.length].y - vertices[i].y
        })
    }

    return edges;
}
/**
 * Calculates the dot product of 2 2D vectors
 * @param {Object} v1 
 * @param {Object} v2 
 */
function dot(v1, v2){
    return v1.x*v2.x+v1.y*v2.y;
}

