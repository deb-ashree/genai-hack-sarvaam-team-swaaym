import json
import sys
from textwrap import dedent
import time
import streamlit as st
# import test  
from app.review_app import ReviewPage
from app.course_spec_app import Home
from app.course_page_app import CoursePage
from server import sendTopicDetails

# Set page configuration
st.set_page_config(page_title="Course Master", layout="wide")

# if st.button("Review"):
#     data = {}
#     data["summary"] = "Evaporation is when a liquid changes into a gas, like when water turns into water vapor. It happens when the tiny water particles get so excited and energetic that they can break free from the liquid and float around in the air as a gas. It's like when you get so excited that you can't sit still and have to run around!"
#     data["course_plan"] = '**Lesson Plan: Evaporation**\n\n**Section 1: Factors Involved**\n\n* **Details:** Evaporation is the process where liquid turns into a gas.\n* **Types:** Factors that affect evaporation include temperature, surface area, and wind speed.\n* **Experiments:** Place water in two containers: one open and one covered. Observe which evaporates faster.\n\n**Section 2: Latent Heat**\n\n* **Details:** Latent heat is the energy needed to turn a liquid into a gas.\n* **Types:** Latent heat varies depending on the substance being evaporated.\n* **Applicability:** Used in air conditioners and refrigerators to cool down air.\n\n**Section 3: Evaporation Rate**\n\n* **Details:** Evaporation rate is how quickly a liquid evaporates.\n* **Types:** Factors that affect evaporation rate include temperature, surface area, and wind speed.\n* **Real-life examples:** Drying clothes on a clothesline or sweat cooling down our bodies.\n\n**Section 4: Applications**\n\n* **Details:** Evaporation is used in many everyday applications.\n* **Types:** Includes air conditioning, cooling systems, desalination, and drying.\n* **Experiments:** Create a mini air conditioner using a fan and a wet cloth.\n\n**Section 5: Environmental Impact**\n\n* **Details:** Evaporation plays a role in the water cycle and climate.\n* **Types:** Evaporation can affect humidity, cloud formation, and precipitation.\n* **Real-life examples:** Evaporation from oceans and rivers contributes to the formation of clouds and rain.'
#     review_app.app(data)
# else:
#     test.app()

st.markdown("""
    <style>
    .container {
        background-color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

main_css = """
<style>
    container {
        background-color: #ADD8E6;
    }
</style>
"""
st.markdown(main_css, unsafe_allow_html=True)

if "data" not in st.session_state :
    st.session_state["data"] = ''

if "state" not in st.session_state :
    st.session_state["state"] = "start"

if st.session_state["state"] == "review":
    print(f"""Data for review : {st.session_state["data"]}""")
    st.session_state["data"] = ReviewPage.app(st.session_state["data"])
elif st.session_state["state"] == "done":
    print(f"""Data for course : {st.session_state["data"]}""")
    course = CoursePage()
    course.app(st.session_state["data"])
else:
    home = Home()
    home.app()

if st.session_state["state"] != "done":
    if st.button('Send'):
        ## For making REST call
        # res = requests.post(url="http://127.0.0.1:8000/topic", data=json.dumps(inputs))

        if st.session_state["state"] == "start":
            ## For a direct function call
            # old_stdout = sys.stdout
            # log_file = open("out.log","w")
            # sys.stdout = log_file
            # old_stdout = sys.stdout
            # log_file = open("out.log","w")
            # sys.stdout = log_file

            # Prepare User Input
            user_input = home.prepareDict()
            start_time = time.process_time()
            print(start_time)
            input = {"input" : user_input}
            data = sendTopicDetails(input)
            print(f"First Data : {data}")
            st.session_state["data"] = data
            # {"input": {"grade": "Grade 3", "subject": "Science", "topic": "Friction", "language": "English", "instructions": "Share the course details basis a primary school kid's level of understanding", "review_status": "Done"}, "topic": "Friction", "summary": "Imagine trying to slide a book across a table. It doesn't move easily, right? That's friction! It's like a tiny force that holds things back when they try to move.  The rougher the surfaces, the stronger the friction. \n", "course_plan": "## Friction: A Force That Holds Us Back (and Helps Us Move!)\n\n**I. Types of Friction**\n\n* **Details:** Friction is a force that opposes motion between two surfaces that are touching. Think of it like a tiny invisible hand that tries to stop things from moving.\n* **Types:**\n    * **Static Friction:** This friction keeps things still. Like when you push a heavy box, it won't move until you push hard enough to overcome static friction.\n    * **Sliding Friction:** This friction happens when two surfaces slide past each other. Like when you push a book across a table, you feel sliding friction.\n    * **Rolling Friction:** This friction happens when something rolls over a surface. Like when you ride your bike, the wheels experience rolling friction.\n* **Experiments:**\n    * **Static Friction:** Try pushing a heavy object (like a chair) across the floor. Notice how it takes more force to get it moving than to keep it moving? That's static friction!\n    * **Sliding Friction:** Rub your hands together. Can you feel the heat? That's sliding friction turning some of the energy into heat.\n    * **Rolling Friction:** Compare pushing a heavy box on wheels versus dragging it across the floor. Which is easier? Rolling friction is much less than sliding friction.\n\n**II. Friction Applications**\n\n* **Applicability:** Friction is important in many things we do every day!\n* **Real-life examples:**\n    * **Walking:** Friction between your shoes and the ground helps you walk without slipping.\n    * **Writing:** Friction between the pencil lead and paper allows you to write.\n    * **Brakes:** Friction between brake pads and wheels helps cars stop.\n\n**III. Friction Measurement**\n\n* **Details:** We can measure friction using a special tool called a \"friction meter\".\n* **Types:**\n    * **Coefficient of Friction:**  This is a number that tells us how much friction there is between two surfaces. A higher number means more friction.\n    * **Friction Force:** This is the actual force of friction acting on an object.\n* **Experiments:**\n    * **Friction Meter:** You can build a simple friction meter using a spring scale and a block. Pull the block across a surface while measuring the force.\n\n**IV. Friction Reduction**\n\n* **Details:** Sometimes we want to reduce friction, like when things need to move smoothly.\n* **Types:**\n    * **Lubrication:** Using oil or grease to make surfaces slippery reduces friction.\n* **Real-life examples:**\n    * **Car Engines:** Oil lubricates moving parts in engines to reduce friction and prevent wear.\n    * **Roller Skates:** Wheels on roller skates have bearings that reduce friction and make them roll smoothly.\n\n**V. Friction in Nature**\n\n* **Details:** Friction is everywhere in nature!\n* **Types:**\n    * **Air Resistance:** Friction between the air and a moving object, like a bird flying.\n    * **Water Resistance:** Friction between water and a moving object, like a boat sailing.\n* **Real-life examples:**\n    * **Leaves Falling:** The shape of leaves helps them fall slowly due to air resistance.\n    * **Fish Swimming:** Fish have scales that reduce water resistance, making them swim faster. \n", "sections_list": ["Types of Friction", " Friction Applications", " Friction Measurement", " Friction Reduction", " Friction in Nature"], "sections": [{"main_topic": "Friction", "section_name": "Types of Friction", "section_details": "Friction is a force that opposes motion between surfaces in contact. There are mainly two types: static friction, which prevents objects from moving when at rest, and kinetic friction, which acts on moving objects. Static friction is stronger than kinetic friction, requiring more force to initiate movement than to maintain it. Rolling friction is a specialized type that occurs between rolling objects and surfaces, minimizing resistance and allowing smooth motion.", "section_summary": "Friction is a force that opposes motion, categorized into static friction (objects at rest), kinetic friction (objects in motion), and rolling friction (objects rolling on surfaces).", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}, {"main_topic": "Friction", "section_name": " Friction Applications", "section_details": "Friction is a force that opposes motion between surfaces in contact. It has numerous applications in our daily lives.  For example, friction allows us to walk, drive cars, and write with pencils. It also plays a crucial role in braking systems, helping vehicles to stop safely. Friction helps hold objects in place, preventing them from sliding or rolling. In industries, friction is used in various applications like grinding, sanding, and polishing.", "section_summary": "Friction is a vital force that plays a significant role in many aspects of our lives, from walking and driving to industrial processes.", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}, {"main_topic": "Friction", "section_name": " Friction Measurement", "section_details": "Friction is a force that resists motion between two surfaces in contact. Measuring friction helps us understand how objects move and interact.  We can measure friction using a device called a tribometer, which applies a known force to a surface and measures the resulting friction. The coefficient of friction is a dimensionless quantity that describes the ratio of frictional force to the normal force pressing the surfaces together.  It helps us predict how much friction will occur between different materials.", "section_summary": "Measuring friction helps us understand how objects move and interact. We use tribometers to measure friction and calculate the coefficient of friction, which helps predict how much friction will occur between surfaces.", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}, {"main_topic": "Friction", "section_name": " Friction Reduction", "section_details": "Friction reduction is a key concept in engineering and physics, aiming to minimize the resistance between surfaces in contact. This can be achieved through various methods like lubrication, using smoother materials, reducing contact area, and incorporating specialized coatings.  Friction reduction plays a vital role in improving efficiency, reducing wear and tear, and enhancing the performance of machines and systems.", "section_summary": "Friction reduction techniques aim to minimize resistance between surfaces, improving efficiency, reducing wear, and enhancing performance in various applications.", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}, {"main_topic": "Friction", "section_name": " Friction in Nature", "section_details": "Friction is a force that opposes motion between two surfaces in contact. It arises from microscopic irregularities and interactions between the surfaces. There are two main types: static friction, which prevents objects from moving, and kinetic friction, which acts on moving objects. Friction is essential in everyday life, allowing us to walk, write, and even drive cars. However, it can also cause wear and tear on surfaces and generate heat.", "section_summary": "Friction is a force that opposes motion between surfaces, essential for everyday activities but also causing wear and tear.", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}]}
            
            st.session_state["state"] = "review"
            end_time = time.process_time()
            print(end_time)
            print(f"Total time taken : {end_time}-{start_time}")
            # print(st.session_state["data"])
            # print(st.session_state["state"])
            # sys.stdout = old_stdout
            # log_file.close()
        
        elif st.session_state["state"] == "review":
            print("Review done, next page ")
            print(f"Reviewed Data : \n {st.session_state['data']}")
            print(type(st.session_state['data']))
            input = json.loads(json.dumps(st.session_state['data']))
            st.session_state["data"] = sendTopicDetails(input)
            # st.session_state["data"] = dedent("""
            #             {"input": {"grade": "Grade 3", "subject": "Science", "topic": "Friction", "language": "English", "instructions": "Share the course details basis a primary school kid's level of understanding", "review_status": "Done"}, "topic": "Friction", "summary": "Imagine you're pushing a box across the floor.  It's harder to move than if it were on ice, right? That's friction! It's a force that opposes motion, like a tiny brake between surfaces that are touching. The rougher the surfaces, the more friction there is! \n", "course_plan": "## Friction: A Force that Holds Us Back (and Helps Us Go!)\n\n**1. Types of Friction**\n\n* **Details:** Friction is a force that happens when two surfaces rub against each other. It makes things slow down or stop moving.\n* **Types:** \n    * **Static Friction:**  Friction that keeps things still. Like when you push a heavy box, but it doesn't move at first.\n    * **Sliding Friction:** Friction when things slide over each other. Like when you push a box across the floor.\n    * **Rolling Friction:** Friction when things roll over each other. Like when you ride a bike.\n* **Experiments:** \n    * **Sliding vs. Rolling:** Try sliding a book across a table and then rolling it. Which is easier? Why?\n    * **Surface Roughness:** Compare sliding a book on a smooth table vs. a rough carpet. Which has more friction?\n\n**2. Friction Applications**\n\n* **Details:**  Friction is helpful in many ways! It keeps us safe and helps us do things.\n* **Real-life Examples:**\n    * **Walking:**  Friction between your shoes and the ground keeps you from slipping.\n    * **Brakes:**  Friction in car brakes helps them stop. \n    * **Writing:**  Friction between the pencil and paper helps you write.\n* **Applicability:**  Friction is used in many things, from toys to cars to buildings!\n\n**3. Friction Measurement**\n\n* **Details:** We can measure how strong friction is!\n* **Experiments:** \n    * **Pulling a Weight:**  Pull a weight across different surfaces (smooth, rough) and measure the force needed.\n    * **Inclined Plane:** Roll a ball down a ramp with different angles. See how the speed changes with the angle.\n* **Applicability:** Measuring friction helps scientists and engineers design safer and more efficient things.\n\n**4. Friction Reduction**\n\n* **Details:** Sometimes friction is bad, like when it makes things wear out. \n* **Types:** \n    * **Lubricants:**  Oils and greases reduce friction between moving parts.\n    * **Smooth Surfaces:**  Making surfaces smoother reduces friction.\n    * **Air Resistance:**  Aerodynamic shapes help reduce friction from air.\n* **Real-life Examples:** \n    * **Oil in Engines:**  Oil reduces friction in car engines, making them run smoothly.\n    * **Streamlined Cars:**  Cars with smooth shapes reduce air resistance, helping them go faster.\n\n**5. Friction Effects**\n\n* **Details:** Friction can have both good and bad effects.\n* **Real-life Examples:**\n    * **Heat:**  Friction creates heat. That's why your hands get warm when you rub them together.\n    * **Wear and Tear:**  Friction causes things to wear out over time. Like the soles of your shoes.\n    * **Sound:**  Friction can create sound, like when you rub your fingers together.\n* **Applicability:** Understanding friction effects helps us design and build things that last longer and work better. \n", "sections_list": ["Types of Friction", " Friction Applications", " Friction Measurement", " Friction Reduction", " Friction Effects"], "sections": [{"main_topic": "Friction", "section_name": "Types of Friction", "section_details": "Friction is a force that opposes motion between two surfaces in contact. There are mainly two types: static friction, which acts on objects at rest, preventing them from moving, and kinetic friction, which acts on objects in motion, slowing them down. Static friction is stronger than kinetic friction, requiring more force to initiate movement. Kinetic friction is further categorized into sliding friction, occurring when surfaces slide past each other, and rolling friction, which occurs when one surface rolls over another, like wheels on a road. ", "section_summary": "Friction, a force opposing motion, comes in two main types: static friction for objects at rest and kinetic friction for moving objects, with further variations like sliding and rolling friction.", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}, {"main_topic": "Friction", "section_name": " Friction Applications", "section_details": "Friction is a force that opposes motion between two surfaces in contact. It's essential for many everyday activities.  For example, walking, driving, and writing all rely on friction.  Without friction, our shoes would slip on the floor, cars wouldn't be able to move, and pencils wouldn't leave a mark on paper.", "section_summary": "Friction is a force that opposes motion, making it crucial for everyday activities like walking, driving, and writing.", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}, {"main_topic": "Friction", "section_name": " Friction Measurement", "section_details": "Measuring friction involves determining the force that opposes motion between two surfaces in contact. This can be done through various methods, including the use of a friction tester, where a known force is applied to an object and the resulting friction force is measured. Alternatively, the coefficient of friction can be calculated by measuring the force required to initiate motion (static friction) or keep an object moving (kinetic friction). Understanding friction measurement is crucial for various applications, including designing machines, predicting wear, and optimizing lubrication.", "section_summary": "Friction measurement helps understand the forces opposing motion between surfaces, crucial for design, wear prediction, and lubrication.", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}, {"main_topic": "Friction", "section_name": " Friction Reduction", "section_details": "Friction is a force that opposes motion between surfaces in contact. While friction is essential in everyday life, reducing friction is crucial in many applications to improve efficiency and minimize wear. This can be achieved through various methods, including lubrication, using smoother surfaces, and employing bearings and rollers.  By understanding the principles of friction and implementing effective reduction techniques, we can optimize the performance of mechanical systems, reduce energy consumption, and enhance overall efficiency.", "section_summary": "Friction reduction techniques aim to minimize the opposing force between surfaces, enhancing efficiency and reducing wear in various applications.", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}, {"main_topic": "Friction", "section_name": " Friction Effects", "section_details": "Friction is a force that opposes motion between two surfaces in contact. It arises from the microscopic irregularities and interactions between the surfaces. The effects of friction are diverse, impacting everyday activities and various engineering applications. It can generate heat, wear down surfaces, and influence the stability of objects. Friction can be beneficial, allowing us to walk, drive, and grip objects. However, it also causes energy loss, leading to decreased efficiency in machines.", "section_summary": "Friction, a force opposing motion between surfaces, has both positive and negative effects, impacting our daily lives and engineering applications by generating heat, wearing surfaces, and influencing object stability.", "section_review": "Done", "summaryVideoURL": "https://d-id-clips-prod.s3.us-west-2.amazonaws.com/auth0%7C66e3c96f591f03116dbd0fc8/clp_JaCwU8atsE_fb22pNYYEY/lily-akobXDF34M.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1727203338&Signature=fGaN6QjkKQCN5VrkPGVEWaQvJYw%3D", "textContentAudioEnURL": "https://gen-ai-data.s3.amazonaws.com/file1.mp3"}]}
            #             """)
            print(f"Reviewed Completed : \n {st.session_state['data']}")
            st.session_state["state"] = "done"
            print("Status changed")
            
        st.rerun()
