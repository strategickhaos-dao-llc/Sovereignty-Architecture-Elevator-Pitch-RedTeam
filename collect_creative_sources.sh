#!/bin/bash
# collect_creative_sources.sh - Download creative resources for Share Factory Studio
# A creative way to collect 30 video editing and content creation resources
# Pattern: curl -L -s for recon-style resource gathering

# Get the script's directory and change to it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

mkdir -p recon/creative_v1

declare -a sources=(
  "sharefactory_guide,https://www.playstation.com/en-us/support/games/sharefactory-studio-ps5/,sharefactory_studio_guide.html"
  "video_editing_basics,https://www.adobe.com/creativecloud/video/discover/video-editing-basics.html,video_editing_basics.html"
  "color_grading_guide,https://www.adobe.com/creativecloud/video/discover/color-grading.html,color_grading_guide.html"
  "transitions_techniques,https://www.adobe.com/creativecloud/video/discover/video-transitions.html,video_transitions.html"
  "audio_mixing,https://www.adobe.com/creativecloud/video/discover/audio-mixing.html,audio_mixing_guide.html"
  "storyboard_templates,https://www.adobe.com/express/create/storyboard,storyboard_templates.html"
  "video_composition,https://www.adobe.com/creativecloud/video/discover/video-composition.html,video_composition.html"
  "motion_graphics,https://www.adobe.com/creativecloud/video/discover/motion-graphics.html,motion_graphics_intro.html"
  "chroma_key,https://www.adobe.com/creativecloud/video/discover/chroma-key.html,chroma_key_guide.html"
  "frame_rate_guide,https://www.adobe.com/creativecloud/video/discover/frame-rate.html,frame_rate_guide.html"
  "aspect_ratios,https://www.adobe.com/creativecloud/video/discover/aspect-ratio.html,aspect_ratios.html"
  "video_formats,https://www.adobe.com/creativecloud/video/discover/video-file-formats.html,video_formats.html"
  "youtube_specs,https://support.google.com/youtube/answer/1722171,youtube_upload_specs.html"
  "tiktok_guidelines,https://www.tiktok.com/creators/creator-portal/en-us/tiktok-content-strategy/content-creation-tips/,tiktok_content_guide.html"
  "instagram_reels,https://creators.instagram.com/grow/best-practices/reels-best-practices,instagram_reels_guide.html"
  "twitch_stream,https://help.twitch.tv/s/article/guide-to-broadcast-health-and-using-twitch-inspector,twitch_broadcast_guide.html"
  "obs_studio_guide,https://obsproject.com/wiki/,obs_studio_wiki.html"
  "davinci_resolve_training,https://www.blackmagicdesign.com/products/davinciresolve/training,davinci_training.html"
  "final_cut_resources,https://support.apple.com/final-cut-pro,final_cut_support.html"
  "premiere_pro_tutorials,https://helpx.adobe.com/premiere-pro/tutorials.html,premiere_tutorials.html"
  "kdenlive_manual,https://docs.kdenlive.org/en/,kdenlive_docs.html"
  "blender_video_editing,https://docs.blender.org/manual/en/latest/video_editing/index.html,blender_vse_docs.html"
  "creative_commons,https://creativecommons.org/about/cclicenses/,creative_commons_licenses.html"
  "royalty_free_music,https://www.youtube.com/audiolibrary,youtube_audio_library.html"
  "pexels_videos,https://www.pexels.com/videos/,pexels_video_library.html"
  "mixkit_assets,https://mixkit.co/,mixkit_free_assets.html"
  "codec_guide,https://trac.ffmpeg.org/wiki/Encode/H.264,ffmpeg_h264_guide.html"
  "ffmpeg_basics,https://ffmpeg.org/documentation.html,ffmpeg_documentation.html"
  "cinematography_basics,https://www.masterclass.com/articles/film-101-understanding-cinematography,cinematography_guide.html"
  "sound_design,https://www.soundsnap.com/blog/sound-design-101-how-to-start-in-sound-design,sound_design_101.html"
)

count=0
success=0
failed=0

echo "🎬 Starting Creative Resources Collection for Share Factory Studio"
echo "📦 Downloading 30 video editing and content creation resources..."
echo ""

for source in "${sources[@]}"; do
  count=$((count + 1))
  IFS=',' read -r id url file <<< "$source"
  echo "[$count/30] Downloading $id..."
  
  if curl -L -s -H "User-Agent: Strategickhaos-Creative-Recon/1.0" -H "Accept: text/html" \
    --max-time 120 --retry 2 --retry-delay 1 \
    "$url" -o "recon/creative_v1/$file"; then
    
    if [ -s "recon/creative_v1/$file" ]; then
      size=$(stat -f%z "recon/creative_v1/$file" 2>/dev/null || stat -c%s "recon/creative_v1/$file")
      if [ "$size" -gt 1000 ]; then
        echo "✅ Success: $file ($size bytes)"
        success=$((success + 1))
      else
        echo "⚠️  Warning: $file too small ($size bytes)"
        failed=$((failed + 1))
      fi
    else
      echo "❌ Failed: $file (empty)"
      failed=$((failed + 1))
    fi
  else
    echo "❌ Failed: $file (curl error)"
    failed=$((failed + 1))
  fi
  
  # Small delay to be respectful to servers
  sleep 0.5
done

echo ""
echo "🎯 CREATIVE COLLECTION COMPLETE:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Total sources: 30"
echo "Successful: $success"
echo "Failed: $failed"
echo "Success rate: $(( success * 100 / 30 ))%"
echo ""
echo "📂 Resources saved to: recon/creative_v1/"
echo "🎨 These resources cover:"
echo "   • Share Factory Studio workflows"
echo "   • Video editing techniques"
echo "   • Content creation best practices"
echo "   • Audio and visual effects"
echo "   • Platform-specific guidelines"
echo "   • Free asset libraries"
echo "   • Professional cinematography"
echo ""
echo "🚀 Use these resources to enhance your creative video projects!"
