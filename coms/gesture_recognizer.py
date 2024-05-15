import mediapipe as mp

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands

def calculate_distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2) ** 0.5

def is_fist(hand_landmarks):
    """Check if the hand is making a fist."""
    palm_center = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    for finger_tip, finger_mcp in [(mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_CMC),
                                   (mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_MCP),
                                   (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_MCP),
                                   (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_MCP),
                                   (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_MCP)]:
        if calculate_distance(hand_landmarks.landmark[finger_tip], palm_center) > calculate_distance(hand_landmarks.landmark[finger_mcp], palm_center):
            return False
    return True

def is_thumbs_up(hand_landmarks):
    """Check if the hand is making a thumbs-up gesture."""
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
    
    if thumb_tip.y < thumb_ip.y < thumb_mcp.y < thumb_cmc.y:  # Thumb is up
        for finger_tip, finger_mcp in [(mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_MCP),
                                       (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_MCP),
                                       (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_MCP),
                                       (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_MCP)]:
            if calculate_distance(hand_landmarks.landmark[finger_tip], thumb_tip) > calculate_distance(hand_landmarks.landmark[finger_mcp], thumb_tip):
                return False
        return True
    return False
