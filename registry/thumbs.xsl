<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:cmd="http://www.clarin.eu/cmd/"
    xmlns:js="http://www.w3.org/2005/xpath-functions"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs math" version="3.0">
    <xsl:output indent="yes" omit-xml-declaration="no"/>
    <xsl:param name="json-uri" select="()"/>
    <!--<xsl:param name="json-uri" select="'file:/Users/akmi/xyz/reviw.json'"/>-->
    <xsl:param name="json" select="unparsed-text($json-uri)"/>
    <xsl:param name="json-xml" select="json-to-xml($json)"/>
    
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- template for the first tag -->
    
    <xsl:template match="cmd:Review" xpath-default-namespace="http://www.w3.org/2005/xpath-functions">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:apply-templates select="node()"/>
            <!--<xsl:if test="./cmd:author=$author">-->
            <xsl:if test="./cmd:author=$json-xml//array[@key='reviews']/map/map[@key='author']/string[@key='name']">
            <xsl:for-each select="$json-xml//array[@key='interactionStatistic']/map">
                    <xsl:if test="./string[@key='interactionType' and text() ='LikeAction']">
                        <cmd:like><xsl:value-of select="./string[@key='interactionType' and text() ='LikeAction']/following-sibling::map/string[@key='name']"/></cmd:like>
                    </xsl:if>
                    <xsl:if test="./string[@key='interactionType' and text() ='DislikeAction']">
                        <cmd:dislike><xsl:value-of select="./string[@key='interactionType' and text() ='DislikeAction']/following-sibling::map/string[@key='name']"/></cmd:dislike>
                    </xsl:if>
                </xsl:for-each>
            </xsl:if>
            <!--</xsl:if>-->
        </xsl:copy>
    </xsl:template>
    <xsl:template match="cmd:like">
        <xsl:choose>
            <xsl:when test="$json-xml//js:array[@key='interactionStatistic'][js:map/js:string[@key='@type']='LikeAction'][.//js:string[@key='name']=current()][.//js:boolean[@key='delete']='true']">
                <!-- NO Op -->
            </xsl:when>
            <xsl:otherwise><xsl:next-match/></xsl:otherwise>
        </xsl:choose>

    </xsl:template>
    <xsl:template match="cmd:dislike">
        <xsl:choose>
            <xsl:when test="$json-xml//js:array[@key='interactionStatistic']/js:map/js:string[@key='interactionType' and text()='DislikeAction']/following-sibling::js:boolean[@key='delete' and text()='true']/preceding-sibling::js:map/js:string[@key='name']=current()">
                <!-- NO Op -->

            </xsl:when>
            <xsl:otherwise><xsl:next-match/></xsl:otherwise>
        </xsl:choose>

    </xsl:template>
</xsl:stylesheet>
