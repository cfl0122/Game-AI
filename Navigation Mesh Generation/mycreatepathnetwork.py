'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *
import math

# Author: Yuen Han Chan.
# Creates a pathnode network that connects the midpoints of each navmesh together
def myCreatePathNetwork(world, agent = None):

    nodes = []
    edges = []
    polys = []

    worldPoints = world.getPoints();
    worldLines = world.getLines();

    obsPoly = []
    obsPoly_line = []
    obsPolyEdges = []
    obsEdge = []

    for obstacle in world.getObstacles():
        obsPoly.append(obstacle.getPoints());
        obsPoly_line.append(obstacle.getLines());
        for o in obstacle.getLines():
            obsPolyEdges.append(o)
        for p in obstacle.getPoints():
            obsEdge.append(p)

    # Draw Polygon
    for worldPoint1 in worldPoints:
        for worldPoint2 in worldPoints:
            if(worldPoint1!=worldPoint2):
                for worldPoint3 in worldPoints:
                    if(worldPoint3!=worldPoint1) and (worldPoint3!=worldPoint2) and (worldPoint1!=worldPoint2):
                        currentPolyHit = checkCollision(worldPoint1,worldPoint2,worldPoint3,worldLines,obsPoly,world,obsPoly_line);
                        if(currentPolyHit==False):
                            addToPolys(worldPoint1,worldPoint2,worldPoint3,worldLines,polys);
                            line1 = (worldPoint1, worldPoint2);
                            line2 = (worldPoint2, worldPoint3);
                            line3 = (worldPoint3, worldPoint1);
                            # add new polygon lines to worldLines
                            appendLineNoDuplicates(line1, worldLines);
                            appendLineNoDuplicates(line2, worldLines);
                            appendLineNoDuplicates(line3, worldLines);

    # # Check for adjacent polygon, comment out as it doesn't work too well
    m=0
    while(m<100):
        polys = mergingPolys(polys);
        m+=1;

    polyCount = 1;

    radius = agent.getMaxRadius();
    # Edges and nodes
    midpointSet = set();
    for poly in polys:
        mp_poly = midPointPoly(poly);
        # drawCross(world.debug,mp_poly)
        currentPolyMidPoint = [];
        for x in range(len(poly)-1):
            mp = midPoint_pt(poly[x],poly[x+1]);
            if(poly[x],poly[x+1]) in obsPolyEdges or (poly[x+1],poly[x]) in obsPolyEdges:
                continue;
            else:
                addLine = True;
                for obs in obsPolyEdges:
                    if ((minimumDistance(obs, mp)) < radius):
                        addLine = False;
                if(addLine):
                    midpointSet.add(mp);
                    currentPolyMidPoint.append(mp)
        mp = midPoint_pt(poly[len(poly)-1],poly[0]);
        if (poly[len(poly)-1],poly[0]) in obsPolyEdges or (poly[0],poly[len(poly)-1]) in obsPolyEdges:
            continue;
        else:
            addLine = True;
            for obs in obsPolyEdges:
                if ((minimumDistance(obs, mp)) < radius):
                    addLine = False;
            if(addLine):
                midpointSet.add(mp);
                currentPolyMidPoint.append(mp)

        # determine if centroid of poly is too close to obs_edge
        addLine = True;
        for obs in obsPolyEdges:
            if ((minimumDistance(obs, mp_poly)) < radius):
                addLine = False;
        if(addLine):
            midpointSet.add(mp_poly);
            currentPolyMidPoint.append(mp_poly)


        for x in range(len(currentPolyMidPoint)-1):
            midPointLine = (currentPolyMidPoint[x],currentPolyMidPoint[x+1]); 
            hit = rayTraceWorldNoEndPoints(midPointLine[0],midPointLine[1],obsPolyEdges);

            addLine = True;
            for obs in obsEdge:
                if ((minimumDistance(midPointLine, obs)) < radius):
                    addLine = False;
            if (addLine==True) and (hit==None):
                appendLineNoDuplicates(midPointLine,edges);            
        # midPointLine = (currentPolyMidPoint[len(currentPolyMidPoint)-1],currentPolyMidPoint[0]);
        # hit = rayTraceWorldNoEndPoints(midPointLine[0],midPointLine[1],obsPolyEdges);
        # addLine = True;
        # for obs in obsEdge:
        #     if ((minimumDistance(midPointLine, obs)) < radius):
        #         addLine = False;
        # if (addLine==True) and (hit==None):
        #     appendLineNoDuplicates(midPointLine,edges); 
            
        for mp in currentPolyMidPoint:
            nodes.append(mp);
        polyCount+=1;

    # check to connect edges of adjacent Nodes.
    existingEdges = []
    for e in edges:
        appendLineNoDuplicates(e,existingEdges);

    for mp in currentPolyMidPoint:
        nodes.append(mp);

    for mp in midpointSet:
        for mp2 in midpointSet:
            if(mp!=mp2):
                line = (mp,mp2);
                hit = rayTraceWorldNoEndPoints(mp,mp2,existingEdges);
                hit2 = rayTraceWorldNoEndPoints(mp,mp2,obsPolyEdges);
                if(hit==None) and (hit2==None):
                    addLine = True;
                    for obs in obsEdge:
                        if ((minimumDistance(line, obs)) < radius):
                            addLine = False;
                    if (addLine==True):
                        appendLineNoDuplicates(line,edges);
                        appendLineNoDuplicates(line,existingEdges);

    for mp in nodes:
        drawCross(world.debug, mp);

    return nodes, edges, polys;


def midPointPoly(poly):
    xSum = 0;
    ySum = 0;
    for x in range(len(poly)-1):
        mp = midPoint_pt(poly[x],poly[x+1]);
        xSum += mp[0];
        ySum += mp[1];
    mp = midPoint_pt(poly[len(poly)-1],poly[0]);
    xSum += mp[0];
    ySum += mp[1];
    xSum/=len(poly);
    ySum/=len(poly);
    midpoint = ((xSum,ySum));
    return midpoint;

def mergingPolys(polys):
    for poly1 in polys:
        for poly2 in polys:
            if(poly1!=poly2):
                polyAdjacent = polygonsAdjacent(poly1,poly2);
                if(polyAdjacent):
                    mergePoly = polyCombine(poly1,poly2);
                    if(mergePoly!=None):
                        if isConvex(mergePoly):
                            polys.remove(poly1);
                            polys.remove(poly2);
                            polys.append(mergePoly);
                            merging = True;
                            return polys
                            break;
                    else:
                        print "poly is null"
    return polys

def clockWisePoly(e):
    xSum = 0
    ySum = 0
    for x in e:
        xSum=xSum+x[0];
        ySum=ySum+x[1];
    xSum/=len(e);
    ySum/=len(e);
    print "e before Sort: ", e
    def algo(e):
        return (math.atan2(e[0] - xSum, e[1] - ySum) + 2 * math.pi) % (2 * math.pi)

    sortedPolygon = e.sort(key=algo)
    print "e after Sort: ", e
    print "sortted Polygon: ", sortedPolygon
    return e;

def checkCollision(worldPoint1,worldPoint2,worldPoint3,worldLines,obsPoly,world,obsPoly_line):
    # Check for line intersection between 3 nodes and worldLines
    line1 = (worldPoint1, worldPoint2);
    line2 = (worldPoint2, worldPoint3);
    line3 = (worldPoint3, worldPoint1);
    line1_r = (worldPoint1, worldPoint2);
    line2_r = (worldPoint2, worldPoint3);
    line3_r = (worldPoint3, worldPoint1);
    possibleHit1 = rayTraceWorldNoEndPoints(worldPoint1,worldPoint2,worldLines);
    possibleHit2 = rayTraceWorldNoEndPoints(worldPoint2,worldPoint3,worldLines);
    possibleHit3 = rayTraceWorldNoEndPoints(worldPoint3,worldPoint1,worldLines);
    if(possibleHit1) and (line1 not in worldLines) and (line1_r not in worldLines):
        return True;
    if(possibleHit2) and (line2 not in worldLines) and (line2_r not in worldLines):
        return True;
    if(possibleHit3) and (line3 not in worldLines) and (line3_r not in worldLines):
        return True;

    # get midpoint of lines formed by 3 nodes
    midPtLine1 = midPoint_line(line1);
    midPtLine2 = midPoint_line(line2);
    midPtLine3 = midPoint_line(line3);

    for obs_poly in obsPoly_line:
        ptOnPoly1 = pointInsidePolygonLines(midPtLine1,obs_poly);
        ptOnPoly2 = pointInsidePolygonLines(midPtLine2,obs_poly);
        ptOnPoly3 = pointInsidePolygonLines(midPtLine3,obs_poly);

    # Check for line intersection between 3 nodes and polygon
    if(ptOnPoly1) and (line1 not in worldLines) and (line1_r not in worldLines):
        return True;
    if(ptOnPoly2) and (line2 not in worldLines) and (line2_r not in worldLines):
        return True;
    if(ptOnPoly3) and (line3 not in worldLines) and (line3_r not in worldLines):
        return True;

    for obstacle in obsPoly_line:
        if pointInsidePolygonLines(midPtLine1,obstacle) and (line1 not in worldLines) and (line1_r not in worldLines):
            return True
        elif pointInsidePolygonLines(midPtLine2,obstacle) and (line2 not in worldLines) and (line2_r not in worldLines):
            return True
        elif pointInsidePolygonLines(midPtLine3,obstacle) and (line3 not in worldLines) and (line3_r not in worldLines):
            return True

    for obstacle in obsPoly:
        if pointOnPolygon(midPtLine1,obstacle) and (line1 not in worldLines) and (line1_r not in worldLines):
            return True
        elif pointOnPolygon(midPtLine2,obstacle) and (line2 not in worldLines) and (line2_r not in worldLines):
            return True
        if pointOnPolygon(midPtLine3,obstacle) and (line3 not in worldLines) and (line3_r not in worldLines):
            return True

    return False;

def addToPolys(worldPoint1,worldPoint2,worldPoint3,worldLines,polys):
    poly1 = (worldPoint1,worldPoint2,worldPoint3);
    poly2 = (worldPoint1,worldPoint3,worldPoint2);
    poly3 = (worldPoint2,worldPoint3,worldPoint1);
    poly4 = (worldPoint2,worldPoint1,worldPoint3);
    poly5 = (worldPoint3,worldPoint2,worldPoint1);
    poly6 = (worldPoint3,worldPoint1,worldPoint2);
    if (poly1 not in polys) and (poly2 not in polys) and (poly3 not in polys) and (poly4 not in polys) and (poly5 not in polys) and (poly6 not in polys):
        polys.append(poly1);


    return polys;

def polyCombine(poly1,poly2):
    newPolyEdge = set();
    newPolyLine = set();
    for points in poly1:
        newPolyEdge.add(points);
    for points in poly2:
        newPolyEdge.add(points);
    e = []
    for npe in newPolyEdge:
        e.append(npe);
    commonPt = e
    print "CommonPt: ", commonPt
    sortedPolygon = clockWisePoly(commonPt);
    return sortedPolygon;

def midPoint_pt(a,b):
    x = (a[0]+b[0])/2
    y = (a[1]+b[1])/2

    return((x,y))

def midPoint_line((a,b)):
    x = (a[0]+b[0])/2
    y = (a[1]+b[1])/2

    return((x,y))